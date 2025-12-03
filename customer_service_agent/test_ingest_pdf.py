"""
Test script for PDF ingestion.
Verifies that PDFs are correctly parsed, chunked, and stored in the Vector DB.
"""
import os
import sys
import logging
from src.database.vector_db import VectorDB
from src.scripts.ingest import main as ingest_main

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pdf_ingestion():
    print("\n--- Testing PDF Ingestion ---")
    
    # 1. Check if PDFs exist
    docs_dir = os.path.join(os.getcwd(), "data", "docs")
    pdf_files = [f for f in os.listdir(docs_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in data/docs. Cannot test PDF ingestion.")
        return
        
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    # 2. Run ingestion
    print("\nRunning ingestion script...")
    try:
        ingest_main()
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        return

    # 3. Verify Vector DB content
    print("\nVerifying Vector DB content...")
    try:
        vector_db = VectorDB()
        
        # Search for content likely to be in the PDFs
        # Assuming "Privacy Policy" or "Data Protection" is in the docs
        test_query = "data protection"
        results = vector_db.search(test_query, limit=5)
        
        if not results:
            print("❌ No results found in Vector DB.")
            return
            
        print(f"Found {len(results)} results for query '{test_query}':")
        
        pdf_found = False
        for doc in results:
            source = doc.metadata.get("source", "unknown")
            print(f"- Source: {source}")
            # print(f"  Content snippet: {doc.page_content[:100]}...")
            
            if source.lower().endswith('.pdf'):
                pdf_found = True
                
        if pdf_found:
            print("\n✅ PDF ingestion verified! Found PDF documents in search results.")
        else:
            print("\n⚠️ Ingestion ran, but no PDF documents were returned in the top results.")
            print("This might be due to the query not matching PDF content or other docs ranking higher.")
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    test_pdf_ingestion()
