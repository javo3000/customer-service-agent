from src.database.vector_db import VectorDB
from langchain_core.documents import Document
from langchain_core.embeddings import FakeEmbeddings
import logging
import shutil
import os

logging.basicConfig(level=logging.INFO)

if os.path.exists("data/chroma_db"):
    try:
        shutil.rmtree("data/chroma_db")
    except:
        pass

try:
    print("Initializing VectorDB with FakeEmbeddings...", flush=True)
    fake_embeddings = FakeEmbeddings(size=1536)
    vdb = VectorDB(embedding_function=fake_embeddings)
    
    print("Adding mock documents...", flush=True)
    docs = [
        Document(page_content="The return policy is 30 days.", metadata={"source": "policy.pdf"}),
        Document(page_content="Shipping is free for orders over $50.", metadata={"source": "shipping.pdf"})
    ]
    vdb.add_documents(docs)
    
    print("Testing Search...", flush=True)
    results = vdb.search("shipping cost")
    print(f"Found {len(results)} results.")
    
except Exception as e:
    print(f"❌ Verification Failed: {e}", flush=True)
