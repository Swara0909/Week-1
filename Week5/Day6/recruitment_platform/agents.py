from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from config import QA_MODEL, RANKING_MODEL, SCREENING_MODEL


SKILL_CATALOG = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "SQL",
    "PostgreSQL",
    "MongoDB",
    "FastAPI",
    "Flask",
    "Django",
    "React",
    "Node.js",
    "LangChain",
    "RAG",
    "LLM",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "REST API",
    "Git",
    "CI/CD",
    "UI/UX",
    "Figma",
]


@tool
def extract_skills(resume: str) -> str:
    """Extract a normalized technical skill list from resume text."""

    found = [skill for skill in SKILL_CATALOG if skill.lower() in resume.lower()]
    if not found:
        return "Extracted Skills: None found"
    return f"Extracted Skills: {', '.join(sorted(dict.fromkeys(found)))}"


def _normalize_terms(text: str) -> set[str]:
    return {
        term.lower()
        for term in re.findall(r"[A-Za-z0-9+.#/-]{3,}", text)
        if term.lower() not in {"and", "the", "for", "with", "you", "your", "are"}
    }


def estimate_fit_score(job_description: str, resume_context: str, extracted_skills: list[str]) -> int:
    job_terms = _normalize_terms(job_description)
    resume_terms = _normalize_terms(resume_context)
    resume_skill_terms = {skill.lower() for skill in extracted_skills}

    skill_overlap = len(job_terms & resume_skill_terms)
    context_overlap = len(job_terms & resume_terms)

    score = (skill_overlap * 16) + (context_overlap * 2)
    score = max(10, min(95, score))
    return int(score)


@dataclass
class AgentOutputs:
    profile: str
    match_analysis: str
    validation_note: str


class ResumeScreeningAgent:
    def __init__(self):
        self.llm = ChatOllama(model=SCREENING_MODEL, temperature=0.2)
        self.profile_prompt = PromptTemplate(
            template="""You are a Resume Screening Agent.

Use the resume context and extract:
1. Technical skills
2. Experience summary
3. Education summary
4. Notable projects
5. Overall profile summary

Resume Context:
{context}

Return a concise but complete screening note with those headings.""",
            input_variables=["context"],
        )
        self.profile_chain = self.profile_prompt | self.llm | StrOutputParser()

    def run(self, context: str) -> str:
        return self.profile_chain.invoke({"context": context})


class CandidateMatchingAgent:
    def __init__(self):
        self.llm = ChatOllama(model=SCREENING_MODEL, temperature=0.3)
        self.prompt = PromptTemplate(
            template="""You are a Candidate Matching Agent.

Compare the candidate against the job description.

Job Description:
{job_description}

Resume Context:
{context}

Screening Note:
{profile}

Extracted Skills:
{skills}

Return:
1. Match Percentage: integer 0-100
2. Strengths: short bullet list
3. Weaknesses: short bullet list
4. Hiring Recommendation: Hire / Maybe / Reject
5. Justification: 3-5 sentences grounded in the resume
""",
            input_variables=["job_description", "context", "profile", "skills"],
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, job_description: str, context: str, profile: str, skills: str) -> str:
        return self.chain.invoke(
            {
                "job_description": job_description,
                "context": context,
                "profile": profile,
                "skills": skills,
            }
        )


class RankingAgent:
    def __init__(self):
        self.llm = ChatOllama(model=RANKING_MODEL, temperature=0.35)
        self.prompt = PromptTemplate(
            template="""You are a Ranking Agent for recruitment.

Rank the candidates from best to worst for the role below.

Job Description:
{job_description}

Candidate Reports:
{candidate_reports}

Return:
1. Ranked list with candidate names
2. One sentence differentiator for each rank
3. Final shortlist recommendation
""",
            input_variables=["job_description", "candidate_reports"],
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, job_description: str, candidate_reports: str) -> str:
        return self.chain.invoke({"job_description": job_description, "candidate_reports": candidate_reports})


class QAValidationAgent:
    def __init__(self):
        self.llm = ChatOllama(model=QA_MODEL, temperature=0.1)
        self.prompt = PromptTemplate(
            template="""You are a QA Validation Agent.

Check whether the analysis is grounded in the provided resume evidence.

Job Description:
{job_description}

Evidence:
{evidence}

Analysis to validate:
{analysis}

Return:
1. Verdict: Pass / Review
2. Hallucination risk: Low / Medium / High
3. Reasoning: 3-5 short sentences
""",
            input_variables=["job_description", "evidence", "analysis"],
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run(self, job_description: str, evidence: str, analysis: str) -> str:
        return self.chain.invoke(
            {
                "job_description": job_description,
                "evidence": evidence,
                "analysis": analysis,
            }
        )
