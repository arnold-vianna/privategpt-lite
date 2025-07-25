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
try:
    text_loader = DirectoryLoader(SOURCE_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents.extend(text_loader.load())
    print(f"[INFO] Loaded {len(documents)} text documents.")
except Exception as e:
    print(f"[WARN] Error loading .txt files: {e}")

# Load .json files
for filename in os.listdir(SOURCE_DIR):
    if filename.endswith(".json"):
        path = os.path.join(SOURCE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                count = 0
                for entry in data:
                    if isinstance(entry, dict) and "description" in entry and "command" in entry:
                        content = f"{entry['description']}\n{entry['command']}"
                        documents.append(Document(page_content=content))
                        count += 1
                print(f"[INFO] Loaded {count} entries from JSON: {filename}")
        except Exception as e:
            print(f"[WARN] Failed to parse {filename}: {e}")

if not documents:
    print("[ERROR] No documents found. Exiting.")
    exit(1)

# Split text
print("[INFO] Splitting documents...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

# Generate embeddings
print("[INFO] Generating embeddings with SentenceTransformer...")
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

# Save index
print(f"[INFO] Saving FAISS index to: {PERSIST_DIR}")
db.save_local(PERSIST_DIR)

def load_vectorstore(persist_directory="data"):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)


print("[✅] Ingestion complete.")
