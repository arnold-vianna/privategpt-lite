import streamlit as st
from ingest import load_vectorstore
import os
import shutil
import subprocess
from langchain.docstore.document import Document

# Set page config
st.set_page_config(page_title="PrivateGPT Lite", page_icon="📄", layout="wide")

# Set source and persist directory
SOURCE_DIR = os.environ.get("SOURCE_DIR", "./source_documents")
PERSIST_DIR = os.environ.get("PERSIST_DIRECTORY", "./data")

# --- Custom UI styling ---
st.markdown("""
    <style>
        .main {
            background-color: #111827;
            color: #ffffff;
        }
        h1 {
            color: #60A5FA;
        }
        .chunk-box {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 10px;
            background-color: #1f2937;
            border: 1px solid #374151;
        }
        input {
            background-color: #374151 !important;
            color: white !important;
        }
        .github-link {
            text-align: right;
            margin-top: -3rem;
        }
    </style>
""", unsafe_allow_html=True)

# Banner and title
st.image("banner.jpeg", use_container_width=True)
st.markdown("<h1>📄 PrivateGPT Lite — Ask Your Documents</h1>", unsafe_allow_html=True)

# GitHub badge
st.markdown("""
<div class="github-link">
    <a href="https://github.com/arnoldvianna/privategpt-lite" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-Repo-black?logo=github&style=for-the-badge" />
    </a>
</div>
""", unsafe_allow_html=True)

# Upload UI
st.markdown("### 📤 Upload New Documents")
uploaded_files = st.file_uploader("Upload `.txt` or `.json` files", type=["txt", "json"], accept_multiple_files=True)

if uploaded_files:
    os.makedirs(SOURCE_DIR, exist_ok=True)

    for uploaded_file in uploaded_files:
        filename = os.path.basename(uploaded_file.name)
        save_path = os.path.join(SOURCE_DIR, filename)

        try:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Saved: `{filename}`")
        except Exception as e:
            st.error(f"❌ Failed to save `{filename}`: {e}")

    # Re-run ingest.py to update index
    with st.spinner("🔄 Rebuilding index..."):
        result = subprocess.run(["python", "ingest.py"], capture_output=True, text=True)

        if result.returncode == 0:
            st.success("✅ Index updated successfully.")
        else:
            st.error("❌ Indexing failed.")
            st.code(result.stderr)

# Load engine with caching
@st.cache_resource
def load_engine():
    return load_vectorstore()

engine = load_engine()

# Input UI
query = st.text_input("🔍 Ask a question about your documents:", placeholder="e.g. How to run nmap?")

if query:
    st.markdown("### 🔎 Top Matching Chunks:")
    results = engine.similarity_search(query, k=5)

    for i, chunk in enumerate(results):
        content = chunk.page_content.strip()
        description = ""
        command = ""

        # Try splitting based on newlines for .json-formatted results
        if "\n" in content:
            lines = content.split("\n", 1)
            description = lines[0]
            command = lines[1] if len(lines) > 1 else ""
        else:
            description = content

        st.markdown(f"""
        <div class="chunk-box">
            <strong>Chunk {i+1}:</strong><br>
            <strong>Description:</strong> {description}<br>
            <strong>Command:</strong><br>
            <code>{command}</code>
        </div>
        """, unsafe_allow_html=True)
