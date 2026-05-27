# Recruitment-Based Resume Assistant

This project combines the earlier resume screening and multi-resume comparator ideas into one recruitment workflow.

It includes:

- document upload for resumes, job descriptions, interview feedback, and candidate profiles
- semantic RAG search over uploaded documents
- four agent roles: screening, matching, ranking, and QA validation
- a FastAPI backend
- a Streamlit recruiter dashboard

## Run backend

```bash
uvicorn api:app --reload
```

## Run Streamlit UI

```bash
streamlit run streamlit_app.py
```

## Notes

- Store uploaded PDFs in the UI or send them to the API upload endpoint.
- The project uses Ollama models for embeddings and chat, so Ollama must be running locally.
