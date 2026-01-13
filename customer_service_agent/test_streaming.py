import requests
import json

def test_stream():
    url = "http://localhost:8000/ask"
    payload = {
        "question": "What does the Nigeria Tax Act 2025 say about Education Tax?",
        "chat_history": []
    }

    print("Sending streaming request...")
    # stream=True allows reading chunks as they arrive
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    data = json.loads(decoded_line[6:])
                    if data["type"] == "token":
                        print(data["content"], end="", flush=True)
                    elif data["type"] == "metadata":
                        meta = data["content"]
                        print(f"\n\n[Metadata] Route: {meta['route']}, Intent: {meta['intent']}")
                    elif data["type"] == "status":
                        print(f"\n[Status] {data['content']}")
                    elif data["type"] == "error":
                        print(f"\n[Error] {data['content']}")

if __name__ == "__main__":
    test_stream()
