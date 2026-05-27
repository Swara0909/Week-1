from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from engine import RecruitmentEngine
from schemas import (
    ChatRequest,
    ChatResponse,
    CandidateAnalysis,
    DocumentType,
    RankRequest,
    RankingResponse,
    ScreenRequest,
    SearchHit,
    SearchRequest,
    UploadResponse,
)


app = FastAPI(title="Recruitment-Based Resume Assistant", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RecruitmentEngine()


@app.get("/health")
def health():
    return {"status": "ok", "documents": len(engine.list_documents()), "candidates": engine.list_candidates()}


@app.get("/documents")
def list_documents():
    return {"documents": engine.list_documents()}


@app.get("/candidates")
def list_candidates():
    return {"candidates": engine.list_candidates()}


@app.post("/documents/upload", response_model=UploadResponse)
async def upload_documents(
    files: list[UploadFile] = File(...),
    document_type: DocumentType = Form(default=DocumentType.resume),
    owner_name: str | None = Form(default=None),
):
    records = []
    for upload in files:
        content = await upload.read()
        if not content:
            raise HTTPException(status_code=400, detail=f"File '{upload.filename}' is empty")
        records.append(engine.ingest_bytes(upload.filename, content, document_type, owner_name))
    return UploadResponse(records=records)


@app.post("/search", response_model=list[SearchHit])
def search_documents(payload: SearchRequest):
    hits = engine.search(
        payload.query,
        owner_name=payload.owner_name,
        document_type=payload.document_type,
        top_k=payload.top_k,
    )
    return hits


@app.post("/screen", response_model=list[CandidateAnalysis])
def screen_candidates(payload: ScreenRequest):
    if payload.candidate_names:
        return [analysis.model_dump() for analysis in engine.screen_candidates(payload.job_description, payload.candidate_names)]
    return [analysis.model_dump() for analysis in engine.screen_candidates(payload.job_description)]


@app.post("/rank", response_model=RankingResponse)
def rank_candidates(payload: RankRequest):
    ranking, summary, validation_note = engine.rank_candidates(payload.job_description, payload.candidate_names or None)
    return RankingResponse(ranking=ranking, summary=summary, validation_note=validation_note)


@app.post("/chat", response_model=ChatResponse)
def chat_with_resumes(payload: ChatRequest):
    answer, hits = engine.chat(payload.question, payload.owner_name)
    return ChatResponse(answer=answer, citations=hits)
