
import langfuse
print(f"Langfuse dir: {dir(langfuse)}")

if "CallbackHandler" in dir(langfuse):
    print("SUCCESS: Found CallbackHandler in langfuse (top level)")
else:
    print("FAILED: CallbackHandler not in langfuse top level")

try:
    from langfuse.decorators import observe
    print("SUCCESS: Found observe decorator")
except ImportError:
    print("FAILED: observe decorator not found")
