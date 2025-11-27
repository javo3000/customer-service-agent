from pymongo import MongoClient
from pymongo.errors import PyMongoError
from src.config import settings
from typing import Optional, Dict, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)

class MongoDBClient:
    _instance: Optional[MongoClient] = None

    @classmethod
    def get_client(cls) -> MongoClient:
        """
        Returns a singleton instance of the MongoClient.
        """
        if cls._instance is None:
            try:
                # str(settings.MONGO_URI) converts MongoDsn to string
                cls._instance = MongoClient(str(settings.MONGO_URI))
                # Trigger a connection check
                cls._instance.admin.command('ping')
                logger.info("Successfully connected to MongoDB.")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise e
        return cls._instance

    @classmethod
    def get_database(cls, db_name: str = "customer_service"):
        """
        Returns the default database.
        """
        client = cls.get_client()
        return client[db_name]

def query_order(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Queries the 'orders' collection for a specific order ID.
    Returns the order document or None if not found.
    """
    try:
        db = MongoDBClient.get_database()
        collection = db["orders"]
        
        # Simple find_one query
        order = collection.find_one({"order_id": order_id})
        
        if order:
            # Convert ObjectId to string for cleaner JSON handling if needed
            if "_id" in order:
                order["_id"] = str(order["_id"])
            return order
        else:
            logger.warning(f"Order {order_id} not found.")
            return None

    except PyMongoError as e:
        logger.error(f"Database error querying order {order_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error querying order {order_id}: {e}")
        return None
