from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_DIR = DATA_DIR / "vectorstore"
MANIFEST_PATH = DATA_DIR / "manifest.json"

for directory in (DATA_DIR, UPLOAD_DIR, VECTOR_DIR):
    directory.mkdir(parents=True, exist_ok=True)

COLLECTION_NAME = "recruitment_documents"
EMBEDDING_MODEL = "nomic-embed-text"
SCREENING_MODEL = "llama3"
RANKING_MODEL = "llama3"
QA_MODEL = "llama3"

CHUNK_SIZE = 750
CHUNK_OVERLAP = 120
TOP_K_RESULTS = 5
