from __future__ import annotations

import html
import re
import tempfile
from pathlib import Path

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


st.set_page_config(
    page_title="Resume Comparator",
    page_icon="📄",
    layout="wide",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(90,79,255,0.20), transparent 28%),
        radial-gradient(circle at top right, rgba(79,172,254,0.14), transparent 22%),
        linear-gradient(180deg, #090912 0%, #0b0d16 48%, #07080e 100%);
    color: #efeef8;
}

.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}

.hero h1 {
    font-size: clamp(2.2rem, 4vw, 4rem);
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0;
    background: linear-gradient(135deg, #f5f2ff 0%, #b7a7ff 35%, #68c7ff 70%, #76f0d0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    margin-top: 0.75rem;
    color: #8d8aa5;
    font-family: 'DM Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.78rem;
}

.banner {
    margin: 1rem 0 1.4rem;
    padding: 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid #24243c;
    background: rgba(15, 16, 29, 0.78);
    color: #c9c6df;
    backdrop-filter: blur(10px);
}

.section-label {
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7c7a9c;
    margin: 0 0 0.7rem;
}

.panel {
    background: rgba(17, 18, 31, 0.88);
    border: 1px solid #26263f;
    border-radius: 18px;
    padding: 1.15rem 1.15rem 1.05rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
}

.panel:hover {
    border-color: #4b45a9;
}

.candidate-name {
    font-size: 1rem;
    font-weight: 800;
    color: #f4f3ff;
    margin-bottom: 0.2rem;
}

.candidate-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #8f8aad;
    margin-bottom: 0.75rem;
}

.chip {
    display: inline-block;
    margin: 4px 6px 0 0;
    padding: 4px 11px;
    border-radius: 999px;
    border: 1px solid #3c3764;
    background: #1a1b2d;
    color: #b8b0ff;
    font-family: 'DM Mono', monospace;
    font-size: 0.77rem;
}

.result-shell {
    margin-top: 1.2rem;
    padding: 1.1rem;
    border: 1px solid #26263f;
    border-radius: 18px;
    background: linear-gradient(180deg, rgba(15,16,29,0.92), rgba(10,11,18,0.96));
}

.result-header {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    align-items: start;
    margin-bottom: 0.95rem;
}

.result-title {
    font-size: 1.05rem;
    font-weight: 800;
    color: #f4f3ff;
}

.result-subtitle {
    margin-top: 0.2rem;
    color: #9a97b4;
    font-family: 'DM Mono', monospace;
    font-size: 0.74rem;
}

.result-highlight {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 0.75rem;
    border-radius: 999px;
    border: 1px solid #3b3762;
    background: #17182a;
    color: #cfc8ff;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
}

.result-box {
    background: rgba(12, 13, 23, 0.9);
    border: 1px solid #2a2a45;
    border-left: 4px solid #7c6aff;
    border-radius: 18px;
    padding: 1.2rem 1.25rem;
    color: #e8e6f7;
    font-family: 'DM Mono', monospace;
    line-height: 1.7;
    white-space: pre-wrap;
}

.result-note {
    margin-top: 0.85rem;
    padding: 0.8rem 0.9rem;
    border-radius: 14px;
    background: rgba(124, 106, 255, 0.08);
    border: 1px solid rgba(124, 106, 255, 0.22);
    color: #d9d6ff;
    font-size: 0.92rem;
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 0.9rem;
    margin: 1rem 0 0.2rem;
}

.summary-card {
    background: rgba(16, 17, 28, 0.92);
    border: 1px solid #25253d;
    border-radius: 16px;
    padding: 1rem;
}

.summary-card .label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8a86a8;
}

.summary-card .value {
    margin-top: 0.35rem;
    font-size: 1.4rem;
    font-weight: 800;
    color: #f4f3ff;
}

.summary-card .hint {
    margin-top: 0.3rem;
    color: #9a97b4;
    font-size: 0.88rem;
}

div.stButton > button {
    background: linear-gradient(135deg, #6d5cff, #7d7bff 52%, #54c8ff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    width: 100%;
}

div.stButton > button:hover {
    opacity: 0.92;
}

[data-testid="stFileUploader"] {
    background: rgba(10, 11, 18, 0.72);
    border: 1px dashed #34335b;
    border-radius: 12px;
    padding: 0.45rem;
}

textarea {
    background: #0b0d16 !important;
    color: #f2f1fb !important;
    border-color: #2d2d49 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


@tool
def extract_skills(resume: str) -> str:
    """Extract technical skills from resume text."""
    skills = [
        "Python", "Java", "C", "C++", "SQL", "Machine Learning",
        "Deep Learning", "Flask", "Django", "React", "Node.js",
        "HTML", "CSS", "JavaScript", "LangChain", "AI", "MongoDB",
    ]
    found = [skill for skill in skills if skill.lower() in resume.lower()]
    return f"Extracted Skills: {', '.join(found)}" if found else "Extracted Skills: None found"


def safe_collection_name(prefix: str, name: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9._-]", "", name).strip("._-")
    collection_name = f"{prefix}_{clean[:40] if clean else 'resume'}"
    return collection_name[:512].strip("._-") or f"{prefix}_resume"


def clean_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def process_resume(pdf_path: str, embeddings, collection_name: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
    )


def get_skills_and_context(vector_store, job_description: str, llm):
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(job_description)
    context = "\n\n".join(doc.page_content for doc in relevant_docs)

    llm_with_tools = llm.bind_tools([extract_skills])
    response = llm_with_tools.invoke(f"Extract all technical skills from this resume:\n{context}")

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "extract_skills":
                return extract_skills.invoke(tool_call["args"]), context

    return extract_skills.invoke({"resume": context}), context


def build_comparison_prompt(candidate_text: str, job_description: str) -> PromptTemplate:
    return PromptTemplate(
        template="""
You are a senior recruiter.

Compare all candidates for the following job.

Job Description:
{job_description}

Candidates:
{candidate_text}

Provide:
1. A side-by-side comparison table with Skills Match, Experience, Strengths, Weaknesses, and Match %.
2. Ranking from best to worst.
3. Final hiring recommendation.
""",
        input_variables=["job_description", "candidate_text"],
    )


def parse_top_match(result_text: str) -> str:
    lines = [line.strip() for line in result_text.splitlines() if line.strip()]
    for line in lines:
        if line.lower().startswith("1.") or line.lower().startswith("top candidate"):
            return line.lstrip("1234567890. ") or line
    return "See comparison below"


st.markdown(
    """
<div class="hero">
    <h1>Resume Comparator</h1>
    <p>multi-resume analysis with side-by-side comparison</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="banner">
Upload multiple PDF resumes in one place, paste the job description, and compare candidates without a side panel.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Resume Uploads</div>', unsafe_allow_html=True)
resume_files = st.file_uploader(
    "Upload one or more resume PDFs",
    type=["pdf"],
    accept_multiple_files=True,
    label_visibility="collapsed",
)

st.markdown('<div class="section-label">Job Description</div>', unsafe_allow_html=True)
job_description = st.text_area(
    "job_description",
    placeholder="Paste the job description here...",
    height=170,
    label_visibility="collapsed",
)

run_button = st.button("Compare Candidates")


if run_button:
    if not resume_files or len(resume_files) < 2:
        st.error("Please upload at least two resume PDFs.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        temp_paths: list[str] = []
        candidates: list[dict] = []

        try:
            with st.spinner("Preparing resumes..."):
                embeddings = OllamaEmbeddings(model="nomic-embed-text")
                llm = ChatOllama(model="qwen2.5", temperature=0.3)

                for index, upload in enumerate(resume_files, start=1):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(upload.read())
                        temp_paths.append(temp_file.name)

                    candidate_name = Path(upload.name).stem
                    collection_name = safe_collection_name(f"c{index}", candidate_name)
                    vector_store = process_resume(temp_paths[-1], embeddings, collection_name)
                    skills, context = get_skills_and_context(vector_store, job_description, llm)
                    candidates.append(
                        {
                            "name": candidate_name,
                            "skills": skills,
                            "context": context,
                            "collection": collection_name,
                        }
                    )

            st.markdown('<div class="summary-grid">', unsafe_allow_html=True)
            summary_cols = st.columns(4)
            summary_values = [
                ("Resumes", str(len(candidates)), "Uploaded and analyzed"),
                ("Job Terms", str(len(set(re.findall(r'[A-Za-z0-9+.#-]{3,}', job_description)))), "Used in comparison"),
                ("Mode", "LLM RAG", "Ollama-powered output"),
                ("Output", "Detailed", "Table + ranking + recommendation"),
            ]
            for column, (label, value, hint) in zip(summary_cols, summary_values):
                with column:
                    st.markdown(
                        f'<div class="summary-card"><div class="label">{html.escape(label)}</div><div class="value">{html.escape(value)}</div><div class="hint">{html.escape(hint)}</div></div>',
                        unsafe_allow_html=True,
                    )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label" style="margin-top:1.2rem;">Candidate Snapshots</div>', unsafe_allow_html=True)
            candidate_cols = st.columns(len(candidates), gap="large")
            for column, candidate in zip(candidate_cols, candidates):
                with column:
                    st.markdown('<div class="panel">', unsafe_allow_html=True)
                    st.markdown(f'<div class="candidate-name">{html.escape(candidate["name"])}</div>', unsafe_allow_html=True)
                    skill_list = candidate["skills"].replace("Extracted Skills: ", "").split(", ")
                    chips = "".join(
                        f'<span class="chip">{html.escape(skill)}</span>'
                        for skill in skill_list
                        if skill and skill != "None found"
                    )
                    st.markdown(chips or '<span class="chip">No skills detected</span>', unsafe_allow_html=True)
                    st.markdown(
                        f'<div class="candidate-meta">Collection: {html.escape(candidate["collection"])}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

            candidate_text = ""
            for index, candidate in enumerate(candidates, start=1):
                candidate_text += (
                    f"\nCandidate {index}: {candidate['name']}\n"
                    f"Resume:\n{candidate['context']}\n"
                    f"Skills:\n{candidate['skills']}\n"
                )

            prompt = build_comparison_prompt(candidate_text, job_description)
            llm_plain = ChatOllama(model="llama3", temperature=0.7)
            chain = prompt | llm_plain | StrOutputParser()

            with st.spinner("Generating comparison..."):
                result_text = chain.invoke(
                    {
                        "job_description": job_description,
                        "candidate_text": candidate_text,
                    }
                )

            display_text = clean_text(result_text)
            top_match = parse_top_match(display_text)

            st.markdown('<div class="result-shell">', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-header"><div><div class="result-title">Comparison Output</div><div class="result-subtitle">Side-by-side ranking and recommendation</div></div><div class="result-highlight">Top insight: {html.escape(top_match)}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown(display_text)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-note">The comparison above is generated from the uploaded resumes and the pasted job description.</div>',
                unsafe_allow_html=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        finally:
            for temp_path in temp_paths:
                try:
                    Path(temp_path).unlink(missing_ok=True)
                except OSError:
                    pass
