from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    resume = "resume"
    job_description = "job_description"
    interview_feedback = "interview_feedback"
    candidate_profile = "candidate_profile"
    other = "other"


class IngestRecord(BaseModel):
    file_name: str
    document_type: DocumentType
    owner_name: str
    source_path: str
    chunks: int


class SearchRequest(BaseModel):
    query: str
    owner_name: str | None = None
    document_type: DocumentType | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class ScreenRequest(BaseModel):
    job_description: str
    candidate_names: list[str] = Field(default_factory=list)


class RankRequest(BaseModel):
    job_description: str
    candidate_names: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    question: str
    owner_name: str | None = None


class UploadResponse(BaseModel):
    records: list[IngestRecord]


class SearchHit(BaseModel):
    ref: int
    owner_name: str
    document_type: DocumentType
    source: str
    page: int | str
    preview: str
    content: str


class CandidateAnalysis(BaseModel):
    candidate_name: str
    skill_summary: str
    experience_summary: str
    education_summary: str
    profile_summary: str
    extracted_skills: list[str]
    fit_score: int
    matching_analysis: str
    validation_note: str
    citations: list[SearchHit]


class RankingEntry(BaseModel):
    candidate_name: str
    fit_score: int
    reasoning: str


class RankingResponse(BaseModel):
    ranking: list[RankingEntry]
    summary: str
    validation_note: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[SearchHit]
