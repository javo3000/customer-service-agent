import time
from langchain_openai import ChatOpenAI
from src.config import settings

def benchmark_latency(prompt="Hello, are you online?"):
    print("Initializing ChatOpenAI with new API configuration...")
    llm = ChatOpenAI(
        model="gpt-oss-20b",
        temperature=0.3,
        api_key=settings.OPENAI_API_KEY_AI_GRID,
        base_url=settings.OPENAI_API_BASE_URL
    )
    
    print(f"Sending request: '{prompt}'")
    start_time = time.time()
    response = llm.invoke(prompt)
    end_time = time.time()
    
    latency = end_time - start_time
    print(f"\nResponse: {response.content}")
    print(f"\nLatency: {latency:.4f} seconds")

if __name__ == "__main__":
    benchmark_latency()
