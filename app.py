import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

# Path where your FAISS index is stored
PERSIST_DIR = "./data"

@st.cache_resource
def load_retriever():
    try:
        st.info("Loading vector store...")
        embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = FAISS.load_local(
            PERSIST_DIR,
            embeddings,
            allow_dangerous_deserialization=True  # Safe if you trust the source
        )
        return vector_store.as_retriever()
    except Exception as e:
        st.error(f"Failed to load FAISS index: {e}")
        return None

# UI
st.set_page_config(page_title="PrivateGPT Lite", layout="centered")
st.title("📄 PrivateGPT Lite — Ask Your Documents")

qa = load_retriever()

if qa is None:
    st.stop()

question = st.text_input("🔍 Ask a question about your documents:")

if question.strip():
    try:
        docs = qa.invoke(question.strip())
        if docs:
            st.markdown("### 🔎 Top Matching Chunks:")
            for i, doc in enumerate(docs[:4]):
                st.markdown(f"**Chunk {i+1}:**\n```\n{doc.page_content.strip()}\n```")
        else:
            st.warning("No relevant information found.")
    except Exception as e:
        st.error(f"An error occurred while searching: {e}")