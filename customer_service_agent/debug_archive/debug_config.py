from src.config import settings
print(f"OPENAI_API_KEY set: {bool(settings.OPENAI_API_KEY)}")
print(f"MONGO_URI: {settings.MONGO_URI}")
