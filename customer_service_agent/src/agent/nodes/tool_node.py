"""
Tool node for executing tools based on state flags.
Handles conditional tool execution, parameter extraction, and error handling.
"""
import logging
import re
from typing import Dict, List
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.agent.state import AgentState
from src.agent.tools import query_order_tool, search_legal_docs_tool
from src.config import settings
from langgraph.config import get_stream_writer

logger = logging.getLogger(__name__)

# Initialize LLM for query refinement
llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=settings.OPENAI_API_KEY_AI_GRID,
    base_url=settings.OPENAI_API_BASE_URL
)

refine_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert search query optimizer. Your goal is to extract the core search keywords and phrases from a user's question to retrieve relevant legal/tax documents. Remove generic context (e.g., 'I am a CEO', 'my company', '5 billion revenue'). Return ONLY the search terms."),
    ("user", "{question}")
])

query_refiner = refine_prompt | llm | StrOutputParser()

async def refine_query(question: str) -> str:
    """Extracts core search keywords from the user question."""
    try:
        refined = await query_refiner.ainvoke({"question": question})
        logger.info(f"Refined query: '{question}' -> '{refined}'")
        return refined
    except Exception as e:
        logger.error(f"Query refinement failed: {e}")
        return question


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


async def tool_node(state: AgentState) -> Dict:
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
            
            # Refine query for better retrieval
            refined_query = await refine_query(question)
            
            # Call the tool with refined query
            result = search_legal_docs_tool(refined_query)
            
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
            
            # Stream search status
            try:
                writer = get_stream_writer()
                writer({"type": "status", "content": f"Searched knowledge base using: {refined_query}"})
            except Exception:
                pass
                
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
    
    # Execute Web Search tool for web queries
    if "web" in needed_sources:
        try:
            from src.agent.tools import web_search_tool
            
            logger.info("Executing web_search_tool")
            
            # Call the web search tool
            result = web_search_tool(question)
            
            # Wrap result in a Document
            doc = Document(
                page_content=result,
                metadata={
                    "source": "web_search",
                    "query": question
                }
            )
            
            # Append to existing documents or create new list
            existing_docs = updates.get("documents", [])
            updates["documents"] = existing_docs + [doc]
            
            # Stream search status
            try:
                writer = get_stream_writer()
                writer({"type": "status", "content": "Web search completed"})
            except Exception:
                pass
            
            # Only log success if result doesn't contain error
            if "Error:" not in result:
                logger.info("Successfully completed web search")
            else:
                logger.warning(f"Web search returned error: {result[:100]}")
            
        except Exception as e:
            logger.error(f"Error executing web_search_tool: {e}")
            
            # Store error as a document
            error_doc = Document(
                page_content=f"Error: Web search failed. {str(e)}",
                metadata={
                    "source": "error",
                    "query": question
                }
            )
            existing_docs = updates.get("documents", [])
            updates["documents"] = existing_docs + [error_doc]
    
    return updates
