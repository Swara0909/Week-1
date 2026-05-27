from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agents import (
    CandidateMatchingAgent,
    QAValidationAgent,
    RankingAgent,
    ResumeScreeningAgent,
    estimate_fit_score,
    extract_skills,
)
from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    MANIFEST_PATH,
    TOP_K_RESULTS,
    UPLOAD_DIR,
    VECTOR_DIR,
)
from schemas import CandidateAnalysis, DocumentType, IngestRecord, RankingEntry, SearchHit


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip()).strip("._-")
    return slug or "record"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _section_excerpt(text: str, heading: str) -> str:
    pattern = re.compile(rf"{heading}[:\-]?\s*(.*?)(?:\n\s*[A-Z][A-Za-z ]+[:\-]|\Z)", re.IGNORECASE | re.DOTALL)
    match = pattern.search(text)
    if not match:
        return text[:250].strip()
    excerpt = match.group(1).strip()
    return excerpt[:250].strip() if len(excerpt) > 250 else excerpt


class RecruitmentEngine:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(VECTOR_DIR),
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
        self.screening_agent = ResumeScreeningAgent()
        self.matching_agent = CandidateMatchingAgent()
        self.ranking_agent = RankingAgent()
        self.qa_agent = QAValidationAgent()
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> list[dict]:
        if MANIFEST_PATH.exists():
            try:
                return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return []
        return []

    def _save_manifest(self) -> None:
        MANIFEST_PATH.write_text(json.dumps(self.manifest, indent=2), encoding="utf-8")

    def _record_file(self, filename: str, content: bytes) -> Path:
        target = UPLOAD_DIR / _safe_slug(filename)
        target.write_bytes(content)
        return target

    def _load_file(self, path: Path) -> list[Document]:
        if path.suffix.lower() == ".pdf":
            return PyPDFLoader(str(path)).load()

        text = path.read_text(encoding="utf-8", errors="ignore")
        return [Document(page_content=text, metadata={"source": str(path), "page": 1})]

    def _split_documents(self, documents: list[Document]) -> list[Document]:
        return self.splitter.split_documents(documents)

    def ingest_bytes(
        self,
        filename: str,
        content: bytes,
        document_type: DocumentType,
        owner_name: str | None = None,
    ) -> IngestRecord:
        owner = owner_name or Path(filename).stem
        stored_path = self._record_file(filename, content)
        documents = self._load_file(stored_path)

        for document in documents:
            document.metadata.update(
                {
                    "owner_name": owner,
                    "document_type": document_type.value,
                    "source": str(stored_path),
                    "filename": stored_path.name,
                    "ingested_at": _now(),
                }
            )

        chunks = self._split_documents(documents)
        for index, chunk in enumerate(chunks, start=1):
            chunk.metadata.update(
                {
                    "owner_name": owner,
                    "document_type": document_type.value,
                    "source": str(stored_path),
                    "filename": stored_path.name,
                    "chunk_index": index,
                }
            )

        if chunks:
            self.vector_store.add_documents(chunks)

        self.manifest.append(
            {
                "file_name": stored_path.name,
                "document_type": document_type.value,
                "owner_name": owner,
                "source_path": str(stored_path),
                "chunks": len(chunks),
                "ingested_at": _now(),
            }
        )
        self._save_manifest()

        return IngestRecord(
            file_name=stored_path.name,
            document_type=document_type,
            owner_name=owner,
            source_path=str(stored_path),
            chunks=len(chunks),
        )

    def ingest_text(
        self,
        text: str,
        title: str,
        document_type: DocumentType,
        owner_name: str | None = None,
    ) -> IngestRecord:
        filename = f"{_safe_slug(title)}.txt"
        return self.ingest_bytes(filename, text.encode("utf-8"), document_type, owner_name or title)

    def list_candidates(self) -> list[str]:
        candidates = {
            row["owner_name"]
            for row in self.manifest
            if row.get("document_type") in {DocumentType.resume.value, DocumentType.candidate_profile.value}
        }
        return sorted(candidates)

    def list_documents(self) -> list[dict]:
        return sorted(self.manifest, key=lambda item: item.get("ingested_at", ""), reverse=True)

    def search(
        self,
        query: str,
        owner_name: str | None = None,
        document_type: DocumentType | None = None,
        top_k: int = TOP_K_RESULTS,
    ) -> list[SearchHit]:
        filters: dict[str, str] = {}
        if owner_name:
            filters["owner_name"] = owner_name
        if document_type:
            filters["document_type"] = document_type.value

        where_filter = self._build_where_filter(filters)

        retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": top_k,
                "fetch_k": max(top_k * 3, top_k),
                **({"filter": where_filter} if where_filter else {}),
            },
        )
        docs = retriever.invoke(query)
        return self._to_hits(docs)

    def _build_where_filter(self, filters: dict[str, str]) -> dict | None:
        if not filters:
            return None
        if len(filters) == 1:
            key, value = next(iter(filters.items()))
            return {key: value}
        return {
            "$and": [{key: value} for key, value in filters.items()]
        }

    def _to_hits(self, docs: list[Document]) -> list[SearchHit]:
        hits: list[SearchHit] = []
        for index, document in enumerate(docs, start=1):
            preview = document.page_content.strip().replace("\n", " ")[:180]
            hits.append(
                SearchHit(
                    ref=index,
                    owner_name=document.metadata.get("owner_name", "Unknown"),
                    document_type=DocumentType(document.metadata.get("document_type", DocumentType.other.value)),
                    source=document.metadata.get("source", ""),
                    page=document.metadata.get("page", document.metadata.get("chunk_index", "?")),
                    preview=f"{preview}..." if len(document.page_content.strip()) > 180 else preview,
                    content=document.page_content.strip(),
                )
            )
        return hits

    def _context_from_hits(self, hits: list[SearchHit]) -> str:
        blocks = []
        for hit in hits:
            blocks.append(
                f"[{hit.ref}] Owner: {hit.owner_name} | Type: {hit.document_type.value} | Page: {hit.page}\n{hit.content}"
            )
        return "\n\n".join(blocks)

    def screen_candidate(self, job_description: str, candidate_name: str) -> CandidateAnalysis:
        hits = self.search(
            job_description,
            owner_name=candidate_name,
            document_type=DocumentType.resume,
            top_k=TOP_K_RESULTS,
        )
        context = self._context_from_hits(hits)
        profile = self.screening_agent.run(context)
        skill_line = extract_skills.invoke({"resume": context})
        extracted_skills = [
            skill.strip()
            for skill in skill_line.replace("Extracted Skills:", "").split(",")
            if skill.strip() and skill.strip().lower() != "none found"
        ]
        match_analysis = self.matching_agent.run(job_description, context, profile, skill_line)
        fit_score = estimate_fit_score(job_description, context, extracted_skills)
        validation_note = self.qa_agent.run(job_description, context, match_analysis)

        return CandidateAnalysis(
            candidate_name=candidate_name,
            skill_summary=skill_line,
            experience_summary=_section_excerpt(profile, "Experience"),
            education_summary=_section_excerpt(profile, "Education"),
            profile_summary=profile,
            extracted_skills=extracted_skills,
            fit_score=fit_score,
            matching_analysis=match_analysis,
            validation_note=validation_note,
            citations=hits,
        )

    def screen_candidates(self, job_description: str, candidate_names: list[str] | None = None) -> list[CandidateAnalysis]:
        names = candidate_names or self.list_candidates()
        return [self.screen_candidate(job_description, candidate_name) for candidate_name in names]

    def rank_candidates(
        self,
        job_description: str,
        candidate_names: list[str] | None = None,
    ) -> tuple[list[RankingEntry], str, str]:
        analyses = self.screen_candidates(job_description, candidate_names)
        sorted_analyses = sorted(analyses, key=lambda item: item.fit_score, reverse=True)

        candidate_reports = []
        for analysis in sorted_analyses:
            candidate_reports.append(
                f"Candidate: {analysis.candidate_name}\n"
                f"Fit Score: {analysis.fit_score}\n"
                f"Skills: {', '.join(analysis.extracted_skills) if analysis.extracted_skills else 'None'}\n"
                f"Analysis:\n{analysis.matching_analysis}\n"
            )

        summary_text = self.ranking_agent.run(job_description, "\n\n".join(candidate_reports))
        validation_note = self.qa_agent.run(
            job_description,
            "\n\n".join(analysis.profile_summary for analysis in sorted_analyses),
            summary_text,
        )

        ranking = [
            RankingEntry(
                candidate_name=analysis.candidate_name,
                fit_score=analysis.fit_score,
                reasoning=analysis.matching_analysis.splitlines()[0] if analysis.matching_analysis.splitlines() else "See full analysis",
            )
            for analysis in sorted_analyses
        ]
        return ranking, summary_text, validation_note

    def chat(self, question: str, owner_name: str | None = None) -> tuple[str, list[SearchHit]]:
        hits = self.search(question, owner_name=owner_name, top_k=TOP_K_RESULTS)
        context = self._context_from_hits(hits)
        answer_prompt = (
            "Answer the recruiter question using ONLY the resume/context evidence below. "
            "Cite sources with [1], [2], etc.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate
        from langchain_ollama import ChatOllama

        llm = ChatOllama(model="llama3", temperature=0.2)
        chain = PromptTemplate(template="{prompt}", input_variables=["prompt"]) | llm | StrOutputParser()
        answer = chain.invoke({"prompt": answer_prompt})
        return answer, hits
