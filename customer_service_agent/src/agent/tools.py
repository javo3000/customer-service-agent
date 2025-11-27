from src.database.mongo_client import query_order
from src.database.vector_db import VectorDB
from typing import Dict, Callable, Any
import logging

logger = logging.getLogger(__name__)

def query_order_tool(order_id: str) -> str:
    """
    Fetches order details from the database.
    
    Args:
        order_id (str): The ID of the order to query.
        
    Returns:
        str: A formatted string containing the order details or an error message.
    """
    try:
        # Strip any whitespace from the order ID
        clean_order_id = order_id.strip()
        
        order = query_order(clean_order_id)
        
        if order:
            return f"Order Found:\nID: {order.get('order_id')}\nStatus: {order.get('status')}\nItems: {order.get('items')}\nTotal: {order.get('total_amount')}"
        else:
            return f"Error: Order with ID '{clean_order_id}' not found."
            
    except Exception as e:
        logger.error(f"Error in query_order_tool: {e}")
        return f"Error: Failed to fetch order details. System error: {str(e)}"

def search_legal_docs_tool(query: str) -> str:
    """
    Searches the knowledge base for relevant legal documents and policies.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: A formatted string containing relevant document snippets.
    """
    try:
        print("DEBUG: Initializing VectorDB...", flush=True)
        # Initialize VectorDB (singleton-like usage for now)
        vdb = VectorDB()
        
        print("DEBUG: Performing search...", flush=True)
        results = vdb.search(query)
        print(f"DEBUG: Search returned {len(results)} results.", flush=True)
        
        if not results:
            return "No relevant documents found."
            
        formatted_results = "Found the following relevant information:\n"
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get('source', 'Unknown Source')
            formatted_results += f"\n{i}. From {source}:\n   \"{doc.page_content}\"\n"
            
        return formatted_results
        
    except Exception as e:
        logger.error(f"Error in search_legal_docs_tool: {e}")
        return f"Error: Failed to search knowledge base. System error: {str(e)}"

# Tool Registry
tools_map: Dict[str, Callable[[str], str]] = {
    "query_order": query_order_tool,
    "search_legal_docs": search_legal_docs_tool
}
