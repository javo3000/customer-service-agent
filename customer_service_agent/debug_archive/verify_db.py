from dotenv import load_dotenv
import os

# Force reload .env
load_dotenv(override=True)

from src.database.mongo_client import MongoDBClient
from src.config import settings

print(f"Testing MongoDB Connection...")
print(f"URI: {settings.MONGO_URI}")

try:
    db = MongoDBClient.get_database()
    print("✅ Connection Successful!")
    print(f"Database Name: {db.name}")
    
    # Test query
    print("Testing query_order...")
    order = MongoDBClient.query_order("12345")
    print(f"Order Query Result: {order}")
    
except Exception as e:
    print(f"❌ Connection Failed: {e}")
