"""
Tool node for executing tools based on state flags.
Handles conditional tool execution, parameter extraction, and error handling.
"""
import re
import logging
from typing import Dict, List
from langchain_core.documents import Document

from src.agent.state import AgentState
from src.agent.tools import query_order_tool, search_legal_docs_tool

logger = logging.getLogger(__name__)


def extract_order_id(question: str) -> str:
    """
    Extract order ID from a question using regex patterns.
    
    Args:
        question: User's question text
        
    Returns:
        Extracted order ID or empty string if not found
    """
    # Common patterns for order IDs
    patterns = [
        r'order[:\s]+([A-Z0-9-]+)',  # "order: ABC123" or "order ABC123"
        r'#([A-Z0-9-]+)',             # "#ABC123"
        r'\b([A-Z]{2,}\d{3,})\b',     # "ABC123" (2+ letters followed by 3+ digits)
        r'\b(\d{6,})\b',              # "123456" (6+ digit numbers)
    ]
    
    question_upper = question.upper()
    
    for pattern in patterns:
        match = re.search(pattern, question_upper)
        if match:
            return match.group(1)
    
    return ""


def tool_node(state: AgentState) -> Dict:
    """
    Executes tools based on needed_sources in state.
    
    Conditionally calls:
    - query_order_tool if 'mongo_db' in needed_sources
    - search_legal_docs_tool if 'vector_db' in needed_sources
    
    Args:
        state: Current agent state
        
    Returns:
        Dictionary with updated mongo_data and/or documents
    """
    needed_sources = state.get("needed_sources", [])
    question = state.get("question", "")
    
    updates = {}
    
    # Execute MongoDB tool for order queries
    if "mongo_db" in needed_sources:
        try:
            logger.info("Executing query_order_tool")
            
            # Extract order ID from question
            order_id = extract_order_id(question)
            
            if not order_id:
                logger.warning("Could not extract order ID from question")
                updates["mongo_data"] = [{
                    "error": "Could not extract order ID from your question. Please provide a valid order number."
                }]
            else:
                # Call the tool
                result = query_order_tool(order_id)
                
                # Store result in mongo_data
                updates["mongo_data"] = [{
                    "order_id": order_id,
                    "result": result,
                    "success": "Error:" not in result
                }]
                
                logger.info(f"Successfully queried order {order_id}")
                
        except Exception as e:
            logger.error(f"Error executing query_order_tool: {e}")
            updates["mongo_data"] = [{
                "error": f"Failed to query order: {str(e)}"
            }]
    
    # Execute VectorDB tool for legal/knowledge base queries
    if "vector_db" in needed_sources:
        try:
            logger.info("Executing search_legal_docs_tool")
            
            # Call the tool
            result = search_legal_docs_tool(question)
            
            # Wrap the result in a Document object to match state type
            # The search_legal_docs_tool returns a formatted string,
            # so we store it as a single document
            doc = Document(
                page_content=result,
                metadata={
                    "source": "vector_db_search",
                    "query": question
                }
            )
            
            updates["documents"] = [doc]
            
            logger.info("Successfully searched knowledge base")
            
        except Exception as e:
            logger.error(f"Error executing search_legal_docs_tool: {e}")
            
            # Store error as a document
            error_doc = Document(
                page_content=f"Error: Failed to search knowledge base. {str(e)}",
                metadata={
                    "source": "error",
                    "query": question
                }
            )
            updates["documents"] = [error_doc]
    
    return updates
