# Enterprise Knowledge Assistant

Mini RAG project for the Day 3 build.

## Features

- Upload one or more PDF files
- Semantic search across all indexed documents
- Ask questions over retrieved context
- Source citations for every answer
- Multi-document retrieval from a single vector store

## Stack

- Streamlit UI
- Chroma vector database
- Sentence-transformers embeddings
- Ollama chat model for generation, with a fallback if Ollama is not running

## Run

1. Install dependencies from `requirements.txt`.
2. Make sure Ollama is running if you want generated answers.
3. Start the app with:

```bash
streamlit run rag_app.py
```

## Notes

- PDFs are chunked by page-aware text splitters so source labels can be shown in the UI.
- Indexed data is stored in `vector_store/` next to the app.