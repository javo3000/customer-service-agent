import langfuse
print(f"Langfuse version: {getattr(langfuse, '__version__', 'unknown')}")
print(f"Langfuse file: {langfuse.__file__}")
print("Attributes in langfuse:")
print(dir(langfuse))

try:
    from langfuse.callback import CallbackHandler
    print("SUCCESS: imported langfuse.callback.CallbackHandler")
except ImportError as e:
    print(f"FAILURE: {e}")

try:
    import langfuse.callback
    print(f"langfuse.callback file: {langfuse.callback.__file__}")
except ImportError as e:
    print(f"Could not import langfuse.callback directly: {e}")
