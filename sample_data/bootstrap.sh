#!/bin/sh

echo "[INFO] Bootstrapping demo data..."

if [ ! -f /app/data/index.faiss ]; then
    echo "[INFO] FAISS index not found. Running ingestion..."
    python ingest.py --source_dir /app/sample_data --persist_dir /app/data
else
    echo "[INFO] FAISS index already exists. Skipping ingestion."
fi

streamlit run app.py --server.port=8501 --server.address=0.0.0.0
