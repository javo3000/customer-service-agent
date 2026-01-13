#!/usr/bin/env python3
"""
Simple Example - OpenAI native client with AI GRID Proxy
"""

from openai import OpenAI
import time
import os

# Configure OpenAI client to use your AI GRID proxy endpoint
# API key should be set as environment variable OPENAI_API_KEY

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Load from environment variable
)

# Text in/ Text out openai/gpt-oss-20b
# Text in / semtantic out: 

# Streaming response
t_start = time.time() 
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant for testing AI GRID proxy."},
        {"role": "user", "content": "Why is AI Grid amazing? :D"},
    ],
    temperature=0.1,
    stream=True
)


print("Assistant:", end=" ", flush=True)
timing=[]
t = t_start
for chunk in stream:
    timing.append(time.time()-t)
    t = time.time()
    # Each chunk contains a delta (partial token)
    delta = chunk.choices[0].delta
    if delta.content:   # Sometimes it's None for role info, etc.
        print(delta.content, end="", flush=True)


print()  # final newline
print("Time to first Byte:", timing[0], " Time per output token:", timing[1])
print("TPS:", len(timing)/sum(timing))
