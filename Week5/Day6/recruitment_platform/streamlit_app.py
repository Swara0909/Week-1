from __future__ import annotations

import streamlit as st

from engine import RecruitmentEngine
from schemas import DocumentType


st.set_page_config(page_title="Recruitment Assistant", page_icon="🎯", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at top left, rgba(28, 85, 180, 0.24), transparent 26%),
        radial-gradient(circle at top right, rgba(14, 160, 138, 0.16), transparent 22%),
        linear-gradient(180deg, #08111d 0%, #0a0f16 48%, #05080d 100%);
    color: #eef3f9;
}

.hero {
    padding: 2rem 0 1rem;
    text-align: center;
}

.hero h1 {
    margin: 0;
    font-size: clamp(2.2rem, 4vw, 4rem);
    font-weight: 800;
    letter-spacing: -1.4px;
    background: linear-gradient(135deg, #f4fbff 0%, #86d8ff 36%, #88f0cc 68%, #f1d77f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    margin-top: 0.75rem;
    color: #8ea5bd;
    font-family: 'DM Mono', monospace;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.78rem;
}

.cardbox {
    padding: 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid #20334a;
    background: rgba(8, 16, 26, 0.76);
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
}

.section-label {
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7d93ad;
    margin: 0.2rem 0 0.65rem;
}

.metric {
    border-radius: 16px;
    border: 1px solid #20334a;
    background: rgba(10, 17, 28, 0.85);
    padding: 0.95rem 1rem;
}

.metric .label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8aa0b5;
}

.metric .value {
    margin-top: 0.35rem;
    font-size: 1.45rem;
    font-weight: 800;
    color: #f7fbff;
}

.metric .hint {
    margin-top: 0.3rem;
    color: #98adbf;
    font-size: 0.88rem;
}
</style>
""",
    unsafe_allow_html=True,
)


def get_engine() -> RecruitmentEngine:
    if "engine" not in st.session_state:
        st.session_state.engine = RecruitmentEngine()
    return st.session_state.engine


def metric_card(label: str, value: str, hint: str) -> str:
    return f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>'


def show_hit(hit):
    st.markdown(
        f"""
<div class="cardbox">
<div class="section-label">Reference {hit.ref}</div>
<strong>{hit.owner_name}</strong> · {hit.document_type.value} · page {hit.page}<br/>
<div style="margin-top:0.6rem; color:#cad7e4;">{hit.preview}</div>
</div>
""",
        unsafe_allow_html=True,
    )


engine = get_engine()

st.markdown(
    """
<div class="hero">
    <h1>Recruitment Intelligence Hub</h1>
    <p>resume upload, rag search, screening agents, ranking, and recruiter chat</p>
</div>
""",
    unsafe_allow_html=True,
)

tab_upload, tab_screen, tab_search, tab_chat = st.tabs(["Upload", "Screen", "Search", "Chat"])

with tab_upload:
    st.markdown('<div class="section-label">Document Upload</div>', unsafe_allow_html=True)
    uploads = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    col_left, col_right = st.columns(2)
    with col_left:
        document_type = st.selectbox(
            "Document type",
            [item.value for item in DocumentType],
            index=0,
        )
    with col_right:
        owner_name = st.text_input(
            "Candidate / profile name",
            placeholder="e.g. Aditi Sharma, UI/UX Lead, Java Backend Team",
        )

    if st.button("Ingest into Knowledge Base", use_container_width=True):
        if not uploads:
            st.error("Upload at least one document first.")
        else:
            for upload in uploads:
                engine.ingest_bytes(
                    upload.name,
                    upload.getvalue(),
                    DocumentType(document_type),
                    owner_name or None,
                )
            st.success(f"Ingested {len(uploads)} document(s).")
            st.rerun()

    st.markdown('<div class="section-label" style="margin-top:1rem;">Recruitment Dashboard</div>', unsafe_allow_html=True)
    docs = engine.list_documents()
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Documents", str(len(docs)), "Indexed items in the vector store"),
        ("Candidates", str(len(engine.list_candidates())), "Resume or profile owners"),
        ("Resumes", str(sum(1 for doc in docs if doc.get("document_type") == DocumentType.resume.value)), "Candidate resume files"),
        ("RAG Store", "Chroma", "Persistent recruiter knowledge base"),
    ]
    for column, (label, value, hint) in zip((c1, c2, c3, c4), metrics):
        with column:
            st.markdown(metric_card(label, value, hint), unsafe_allow_html=True)

    if docs:
        st.dataframe(docs, use_container_width=True, hide_index=True)

with tab_screen:
    st.markdown('<div class="section-label">Candidate Screening</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "job_description",
        placeholder="Paste the job description here...",
        height=180,
        label_visibility="collapsed",
    )

    available_candidates = engine.list_candidates()
    selected_candidates = st.multiselect(
        "Choose candidates to screen",
        options=available_candidates,
        default=available_candidates[:5],
    )

    if st.button("Run Screening + Ranking", use_container_width=True):
        if not job_description.strip():
            st.error("Enter a job description first.")
        elif not selected_candidates:
            st.error("Upload resumes and select at least one candidate.")
        else:
            with st.spinner("Running agents..."):
                analyses = engine.screen_candidates(job_description, selected_candidates)
                ranking, summary, validation_note = engine.rank_candidates(job_description, selected_candidates)

            st.markdown('<div class="cardbox">', unsafe_allow_html=True)
            st.markdown("<div class='section-label'>Ranking Summary</div>", unsafe_allow_html=True)
            st.write(summary)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-label" style="margin-top:1rem;">Candidate Fit Scores</div>', unsafe_allow_html=True)
            st.table([
                {
                    "Candidate": item.candidate_name,
                    "Fit Score": item.fit_score,
                    "Recommendation": item.matching_analysis.splitlines()[3] if len(item.matching_analysis.splitlines()) > 3 else "See analysis",
                }
                for item in analyses
            ])

            st.markdown('<div class="section-label" style="margin-top:1rem;">Detailed Analysis</div>', unsafe_allow_html=True)
            for analysis in analyses:
                with st.expander(f"{analysis.candidate_name} - {analysis.fit_score}% fit"):
                    st.write(analysis.profile_summary)
                    st.write(analysis.matching_analysis)
                    st.write(analysis.validation_note)
                    for hit in analysis.citations:
                        show_hit(hit)

            st.markdown('<div class="section-label" style="margin-top:1rem;">Final Validation</div>', unsafe_allow_html=True)
            st.write(validation_note)

            st.markdown('<div class="section-label" style="margin-top:1rem;">Final Ranking</div>', unsafe_allow_html=True)
            st.table([entry.model_dump() for entry in ranking])

with tab_search:
    st.markdown('<div class="section-label">Semantic Search</div>', unsafe_allow_html=True)
    query = st.text_input(
        "Search query",
        placeholder="Example: Python + RAG experience or UI/UX role",
    )
    filter_owner = st.selectbox("Filter by candidate/profile", options=["All"] + engine.list_candidates())

    if st.button("Search Knowledge Base", use_container_width=True):
        if not query.strip():
            st.error("Enter a search query.")
        else:
            owner_name = None if filter_owner == "All" else filter_owner
            hits = engine.search(query, owner_name=owner_name)
            if not hits:
                st.info("No relevant documents found.")
            else:
                for hit in hits:
                    show_hit(hit)

with tab_chat:
    st.markdown('<div class="section-label">Resume Chatbot</div>', unsafe_allow_html=True)
    question = st.text_input("Ask about a candidate or resume", placeholder="Does this candidate know LangChain?")
    chat_filter = st.selectbox("Optional candidate filter", options=["All"] + engine.list_candidates(), key="chat_filter")

    if st.button("Ask", use_container_width=True):
        if not question.strip():
            st.error("Ask a question first.")
        else:
            owner_name = None if chat_filter == "All" else chat_filter
            answer, hits = engine.chat(question, owner_name=owner_name)
            st.markdown('<div class="cardbox">', unsafe_allow_html=True)
            st.write(answer)
            st.markdown('</div>', unsafe_allow_html=True)
            for hit in hits:
                show_hit(hit)