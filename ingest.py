import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

SOURCE_DIR = os.environ.get("SOURCE_DIR", "./source_documents")
PERSIST_DIR = os.environ.get("PERSIST_DIRECTORY", "./data")

print(f"[INFO] Loading documents from: {SOURCE_DIR}")

documents = []

# Load .txt files
text_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.txt", loader_cls=TextLoader)
try:
    documents.extend(text_loader.load())
except Exception as e:
    print(f"[WARN] Error loading .txt files: {e}")

# Manually load JSON files formatted as list of {description, command}
for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".json"):
        path = os.path.join(SOURCE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    if isinstance(entry, dict) and "description" in entry and "command" in entry:
                        content = f"{entry['description']}\n{entry['command']}"
                        documents.append(Document(page_content=content))
        except Exception as e:
            print(f"[WARN] Failed to parse {filename}: {e}")

if not documents:
    print("[WARN] No documents found. Exiting.")
    exit(0)

# Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Generate embeddings
print("[INFO] Generating embeddings...")
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

# Save the vector index
print(f"[INFO] Saving FAISS index to: {PERSIST_DIR}")
db.save_local(PERSIST_DIR)

print("[✅] Ingestion complete.")
