import langfuse
import pkgutil
import inspect

print(f"Searching in: {langfuse.__path__}")

def find_callback_handler(package):
    for importer, modname, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = __import__(modname, fromlist="dummy")
            if hasattr(module, "CallbackHandler"):
                print(f"FOUND CallbackHandler in: {modname}")
            if hasattr(module, "LangfuseCallbackHandler"):
                print(f"FOUND LangfuseCallbackHandler in: {modname}")
        except Exception as e:
            pass # Ignore import errors

find_callback_handler(langfuse)
