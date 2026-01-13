import os
from dotenv import load_dotenv

load_dotenv()

vars_to_check = [
    "OPENAI_API_BASE_URL",
    "OPENAI_API_KEY_AI_GRID",
    "LANGFUSE_PUBLIC_KEY",
    "LANGFUSE_SECRET_KEY",
    "LANGFUSE_HOST"
]

print("--- Environment Variable Diagnostics ---")
for var in vars_to_check:
    val = os.getenv(var)
    if val:
        # Mask key for safety
        masked = val[:5] + "..." + val[-4:] if len(val) > 10 else "SET"
        print(f"{var}: {masked}")
    else:
        print(f"{var}: NOT SET")
