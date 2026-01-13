
import sys
import os
import time
from dotenv import load_dotenv

# Load env vars manually just in case
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd())))

from src.database.vector_db import VectorDB

def debug_search():
    print("DEBUG: Starting...", flush=True)
    try:
        print("DEBUG: Initializing VectorDB...", flush=True)
        vdb = VectorDB()
        print("DEBUG: VectorDB initialized.", flush=True)
        
        query = "CIT PAYE PIT payment schedule due date monthly yearly filing returns"
        
        print(f"\nQuery: {query}\n", flush=True)
        print("-" * 50, flush=True)
        
        # Try with default limit
        print("DEBUG: Searching with limit=5...", flush=True)
        results = vdb.search(query, limit=5)
        print(f"DEBUG: Found {len(results)} results.", flush=True)
        
        for i, doc in enumerate(results, 1):
            print(f"\nResult {i}:", flush=True)
            print(f"Source: {doc.metadata.get('source')}", flush=True)
            print(f"Content: {doc.page_content}", flush=True)
            
        print("-" * 50, flush=True)
        
    except Exception as e:
        print(f"ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_search()
