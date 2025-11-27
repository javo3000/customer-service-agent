from langchain_openai import OpenAIEmbeddings
from src.config import settings
import time
import logging

logging.basicConfig(level=logging.INFO)

try:
    print("Initializing OpenAIEmbeddings...", flush=True)
    embeddings = OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY.get_secret_value()
    )
    print("OpenAIEmbeddings initialized.", flush=True)
    
    print("Sleeping...", flush=True)
    time.sleep(5)
    print("Woke up!", flush=True)
    
    vec = embeddings.embed_query("test")
    print(f"✅ Embed success. Len: {len(vec)}")
    
except Exception as e:
    print(f"❌ Failed: {e}")
