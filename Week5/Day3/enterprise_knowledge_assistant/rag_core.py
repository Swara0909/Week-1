from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

try:
    from langchain_ollama import ChatOllama
except Exception:  # pragma: no cover - optional dependency fallback
    ChatOllama = None


@dataclass
class DocumentHit:
    source_name: str
    page_number: int
    snippet: str
    score: float
    metadata: dict


@dataclass
class IngestionResult:
    files_indexed: int
    documents_indexed: int


@dataclass
class AnswerResult:
    question: str
    answer: str
    citations: List[str]
    retrieved_chunks: List[DocumentHit]


def _safe_metadata_value(value: object, default: str = "Unknown") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text or default


class KnowledgeAssistant:
    def __init__(
        self,
        persist_directory: str = "vector_store",
        collection_name: str = "enterprise_knowledge",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        chat_model: str = "llama3",
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        top_k: int = 5,
    ) -> None:
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self._vectorstore: Chroma | None = None
        self._embeddings: HuggingFaceEmbeddings | None = None

    @property
    def store_path(self) -> Path:
        return Path(self.persist_directory)

    def _embedding_function(self) -> HuggingFaceEmbeddings:
        if self._embeddings is None:
            self._embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
        return self._embeddings

    def _build_vectorstore(self) -> Chroma:
        return Chroma(
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
            embedding_function=self._embedding_function(),
        )

    @property
    def vectorstore(self) -> Chroma:
        if self._vectorstore is None:
            self._vectorstore = self._build_vectorstore()
        return self._vectorstore

    def _split_documents(self, documents: Sequence[Document]) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        return splitter.split_documents(list(documents))

    def ingest_pdfs(self, pdf_paths: Iterable[Path]) -> IngestionResult:
        all_documents: List[Document] = []
        pdf_paths = list(pdf_paths)

        for pdf_path in pdf_paths:
            loader = PyPDFLoader(str(pdf_path))
            documents = loader.load()
            for document in documents:
                document.metadata["source_name"] = pdf_path.name
            all_documents.extend(documents)

        if not all_documents:
            return IngestionResult(files_indexed=0, documents_indexed=0)

        chunks = self._split_documents(all_documents)
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = index
            chunk.metadata["source_name"] = _safe_metadata_value(
                chunk.metadata.get("source_name"),
                default=Path(chunk.metadata.get("source", "document.pdf")).name,
            )

        self.vectorstore.add_documents(chunks)
        self.vectorstore.persist()

        return IngestionResult(files_indexed=len(pdf_paths), documents_indexed=len(chunks))

    def _format_hit(self, document: Document, score: float) -> DocumentHit:
        source_name = _safe_metadata_value(document.metadata.get("source_name"))
        page_number = int(document.metadata.get("page", 0)) + 1
        snippet = document.page_content.strip().replace("\n", " ")
        if len(snippet) > 350:
            snippet = snippet[:347].rstrip() + "..."
        return DocumentHit(
            source_name=source_name,
            page_number=page_number,
            snippet=snippet,
            score=score,
            metadata=document.metadata,
        )

    def search(self, query: str, top_k: int | None = None) -> List[DocumentHit]:
        if not query.strip():
            return []

        results = self.vectorstore.similarity_search_with_relevance_scores(
            query,
            k=top_k or self.top_k,
        )
        return [self._format_hit(document, score) for document, score in results]

    def _build_llm(self):
        if ChatOllama is None:
            return None
        return ChatOllama(model=self.chat_model, temperature=0.1)

    def _citation_labels(self, hits: Sequence[DocumentHit]) -> List[str]:
        labels: List[str] = []
        seen: set[str] = set()
        for hit in hits:
            label = f"{hit.source_name} - page {hit.page_number}"
            if label not in seen:
                seen.add(label)
                labels.append(label)
        return labels

    def _answer_with_llm(self, question: str, hits: Sequence[DocumentHit]) -> str:
        context = "\n\n".join(
            f"Source: {hit.source_name} | Page: {hit.page_number}\n{hit.snippet}"
            for hit in hits
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an enterprise knowledge assistant. Answer only from the provided context. Cite sources inline using the exact source name and page number. If the context is insufficient, say what is missing.",
                ),
                (
                    "human",
                    "Question: {question}\n\nContext:\n{context}",
                ),
            ]
        )

        llm = self._build_llm()
        if llm is None:
            raise RuntimeError("ChatOllama is unavailable")

        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"question": question, "context": context}).strip()

    def _fallback_answer(self, question: str, hits: Sequence[DocumentHit]) -> str:
        if not hits:
            return "No indexed document chunks matched the question yet. Upload PDFs first."

        top_sources = self._citation_labels(hits)
        summary_lines = [
            "I found the following relevant sources:",
            *[f"- {source}" for source in top_sources[:5]],
            "",
            "Most relevant excerpt:",
            hits[0].snippet,
        ]
        return "\n".join(summary_lines)

    def answer(self, question: str, top_k: int | None = None) -> AnswerResult:
        hits = self.search(question, top_k=top_k)
        try:
            answer = self._answer_with_llm(question, hits)
        except Exception:
            answer = self._fallback_answer(question, hits)

        return AnswerResult(
            question=question,
            answer=answer,
            citations=self._citation_labels(hits),
            retrieved_chunks=hits,
        )

    def clear_index(self) -> None:
        self._vectorstore = None
        if self.store_path.exists():
            shutil.rmtree(self.store_path, ignore_errors=True)

    def stats(self) -> dict:
        if not self.store_path.exists():
            return {"chunks": 0, "files": 0}

        try:
            store = self.vectorstore
            collection = store._collection  # type: ignore[attr-defined]
            count = collection.count()
        except Exception:
            count = 0

        return {"chunks": count, "files": count}