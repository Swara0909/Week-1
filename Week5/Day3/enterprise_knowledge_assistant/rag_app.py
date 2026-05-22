from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Iterable, List, Sequence

import streamlit as st

from rag_core import AnswerResult, DocumentHit, KnowledgeAssistant


st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)


def render_hit(hit: DocumentHit, index: int) -> None:
    with st.container(border=True):
        st.markdown(f"**{index}. {hit.source_name}**")
        st.caption(f"Page {hit.page_number} · Score {hit.score:.3f}")
        st.write(hit.snippet)


def format_citations(citations: Sequence[str]) -> str:
    if not citations:
        return "No citations were returned."
    return "\n".join(f"- {citation}" for citation in citations)


def ensure_state() -> KnowledgeAssistant:
    if "assistant" not in st.session_state:
        st.session_state.assistant = KnowledgeAssistant()
    return st.session_state.assistant


def ingest_uploaded_files(assistant: KnowledgeAssistant, uploads: Iterable[object]) -> None:
    uploads = list(uploads)
    if not uploads:
        st.warning("Upload one or more PDF files first.")
        return

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_paths: List[Path] = []
        for upload in uploads:
            temp_path = Path(temp_dir) / upload.name
            temp_path.write_bytes(upload.getbuffer())
            temp_paths.append(temp_path)

        result = assistant.ingest_pdfs(temp_paths)

    st.success(
        f"Indexed {result.documents_indexed} chunks from {result.files_indexed} PDF file(s)."
    )
    st.caption(
        f"Collection: {assistant.collection_name} | Persisted at: {assistant.persist_directory}"
    )


def show_answer(result: AnswerResult) -> None:
    st.subheader("Answer")
    st.markdown(result.answer)
    st.subheader("Citations")
    st.markdown(format_citations(result.citations))


def main() -> None:
    assistant = ensure_state()

    st.title("Enterprise Knowledge Assistant")
    st.write(
        "Upload PDFs, search semantically across them, and ask questions with source citations."
    )

    with st.sidebar:
        st.header("Library Settings")
        assistant.persist_directory = st.text_input(
            "Vector store folder",
            value=assistant.persist_directory,
        )
        assistant.collection_name = st.text_input(
            "Collection name",
            value=assistant.collection_name,
        )
        assistant.embedding_model = st.text_input(
            "Embedding model",
            value=assistant.embedding_model,
        )
        assistant.chat_model = st.text_input(
            "Chat model",
            value=assistant.chat_model,
        )
        assistant.chunk_size = st.slider("Chunk size", 400, 2000, assistant.chunk_size, 100)
        assistant.chunk_overlap = st.slider(
            "Chunk overlap", 0, 400, assistant.chunk_overlap, 25
        )
        assistant.top_k = st.slider("Top-k retrieval", 2, 12, assistant.top_k, 1)
        st.divider()
        if st.button("Clear indexed knowledge", type="secondary"):
            assistant.clear_index()
            st.session_state.pop("last_answer", None)
            st.success("Knowledge base cleared.")

    upload_col, search_col = st.columns([1, 1])

    with upload_col:
        st.subheader("1. Upload PDFs")
        uploads = st.file_uploader(
            "Choose one or more PDFs",
            type=["pdf"],
            accept_multiple_files=True,
        )
        if st.button("Index PDFs", type="primary"):
            ingest_uploaded_files(assistant, uploads or [])

    with search_col:
        st.subheader("2. Search or Ask")
        query = st.text_input("Enter a question or semantic search query")
        search_button = st.button("Search documents")
        ask_button = st.button("Ask question")

        if search_button and query:
            hits = assistant.search(query)
            st.session_state.last_hits = hits
            st.session_state.last_query = query
            if not hits:
                st.info("No matching passages found yet.")
            else:
                st.markdown("### Relevant passages")
                for index, hit in enumerate(hits, start=1):
                    render_hit(hit, index)

        if ask_button and query:
            result = assistant.answer(query)
            st.session_state.last_answer = result
            st.session_state.last_query = query

    if "last_answer" in st.session_state:
        show_answer(st.session_state.last_answer)

    if "last_hits" in st.session_state and st.session_state.last_hits:
        st.subheader("Retrieved context")
        for index, hit in enumerate(st.session_state.last_hits, start=1):
            render_hit(hit, index)

    stats = assistant.stats()
    st.caption(
        f"Indexed chunks: {stats['chunks']} | Indexed files: {stats['files']} | Ready for multi-document retrieval"
    )


if __name__ == "__main__":
    main()