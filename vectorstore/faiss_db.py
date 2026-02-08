# This file handles creation and loading of FAISS vector DB

from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings

def create_faiss_db(text_chunks):
    # Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    # Store chunks into FAISS
    db = FAISS.from_texts(text_chunks, embedding=embeddings)
    return db
