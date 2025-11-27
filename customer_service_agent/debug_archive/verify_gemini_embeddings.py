from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import settings
import time

try:
    print("Initializing Embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.GOOGLE_API_KEY.get_secret_value()
    )
    
    max_retries = 3
    for i in range(max_retries):
        try:
            print(f"Embedding query (Attempt {i+1}/{max_retries})...")
            vec = embeddings.embed_query("Hello world")
            print(f"✅ Embedding successful! Vector length: {len(vec)}")
            break
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                wait_time = 2 ** i
                print(f"⚠️ Quota hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    else:
        print("❌ Failed after max retries.")
    
except Exception as e:
    print(f"❌ Embedding failed: {e}")
