"""
Script to ingest documents from data/docs into the Vector DB.
Supports .txt, .md, and .pdf files.
Implements chunking for better retrieval.
"""
import os
import sys
import logging
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.database.vector_db import VectorDB

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOCS_DIR = os.path.join(os.getcwd(), "data", "docs")

def load_documents() -> List[Document]:
    """Load and chunk documents from the docs directory."""
    documents = []
    
    if not os.path.exists(DOCS_DIR):
        logger.warning(f"Documents directory not found: {DOCS_DIR}")
        return []
        
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    for filename in os.listdir(DOCS_DIR):
        file_path = os.path.join(DOCS_DIR, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        try:
            raw_docs = []
            if filename.lower().endswith('.pdf'):
                logger.info(f"Processing PDF: {filename}")
                loader = PyPDFLoader(file_path)
                raw_docs = loader.load()
            elif filename.lower().endswith(('.txt', '.md')):
                logger.info(f"Processing Text: {filename}")
                loader = TextLoader(file_path, encoding='utf-8')
                raw_docs = loader.load()
            else:
                continue
                
            # Chunk the documents
            chunked_docs = text_splitter.split_documents(raw_docs)
            
            # Add source metadata if missing (PyPDFLoader adds it, TextLoader adds it)
            for doc in chunked_docs:
                if "source" not in doc.metadata:
                    doc.metadata["source"] = filename
            
            documents.extend(chunked_docs)
            logger.info(f"Loaded and chunked {filename} into {len(chunked_docs)} segments.")
            
        except Exception as e:
            logger.error(f"Error reading {filename}: {e}")
            
    return documents

def main():
    logger.info("Starting document ingestion...")
    
    # Load and chunk documents
    docs = load_documents()
    
    if not docs:
        logger.warning("No documents found to ingest.")
        return
        
    # Initialize DB
    try:
        vector_db = VectorDB()
        
        # Add to DB
        vector_db.add_documents(docs)
        
        logger.info(f"Successfully ingested {len(docs)} document chunks.")
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")

if __name__ == "__main__":
    main()
