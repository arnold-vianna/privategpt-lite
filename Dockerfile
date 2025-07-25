FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project into image (including source_documents and data)
COPY . .

# Make sure any scripts are executable
RUN chmod +x ./sample_data/bootstrap.sh

# On container start: run ingestion if needed, then start Streamlit
CMD ["/bin/sh", "-c", "\
  if [ ! -f /app/data/index.faiss ]; then \
    echo '[INFO] Running document ingestion...'; \
    python ingest.py --source_dir /app/source_documents --persist_dir /app/data; \
  else \
    echo '[INFO] FAISS index already exists. Skipping ingestion.'; \
  fi && \
  streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
