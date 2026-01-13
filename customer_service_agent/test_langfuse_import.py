try:
    import langfuse
    print(f"Langfuse imported. Location: {langfuse.__file__}")
    from langfuse.callback import CallbackHandler
    print("CallbackHandler imported successfully.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
