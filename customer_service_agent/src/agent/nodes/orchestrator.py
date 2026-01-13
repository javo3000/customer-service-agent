"""
Orchestrator node for routing customer service queries.
Performs keyword-based routing and intent classification.
"""
from typing import Dict, List
from src.agent.state import AgentState


from langgraph.config import get_stream_writer

async def orchestrator(state: AgentState) -> Dict:
    """
    Routes queries based on keyword matching and updates state with:
    - route: 'order_inquiry', 'legal_inquiry', 'web_search', etc.
    - intent: classified intent
    - needed_sources: list of required data sources
    
    Also handles reroute flag from generate node when context is insufficient.
    
    Args:
        state: Current agent state with user question
        
    Returns:
        Dictionary with route, intent, and needed_sources updates
    """
    question = state.get("question", "").lower()
    needs_web_search = state.get("needs_web_search", False)
    
    # Stream "thinking" status for frontend spinner
    try:
        writer = get_stream_writer()
        writer({"type": "thinking", "content": True})
    except Exception:
        pass
    
    # If generate node flagged for web search (reroute), prioritize web search
    if needs_web_search:
        result = {
            "route": "web_search",
            "intent": "web_search_fallback",
            "needed_sources": ["web"],
            "needs_web_search": False  # Reset the flag
        }
        
        # Stream metadata
        try:
            writer = get_stream_writer()
            writer({"type": "status", "content": "Searching the web for more information..."})
            writer({"type": "metadata", "content": result})
        except Exception:
            pass
            
        return result
    
    # Keyword sets for routing
    order_keywords = {
        "order", "status", "shipping", "delivery", "track", "package",
        "shipment", "tracking", "delivered", "ship", "arrive", "when"
    }
    
    legal_keywords = {
        "legal", "terms", "privacy", "policy", "policies", "agreement",
        "terms of service", "tos", "gdpr", "data", "rights", "refund policy",
        "tax", "act", "taxation", "education", "levy"
    }
    
    # Web search keywords (for keyword-triggered web search)
    web_search_keywords = {
        "search", "lookup", "google", "latest", "news", "current",
        "find online", "recent", "today", "2024", "2025", "2026"
    }
    
    # Determine route based on keyword presence
    route = "general_inquiry"  # default
    intent = "unknown"
    needed_sources = []
    
    # Count keyword matches
    order_matches = sum(1 for keyword in order_keywords if keyword in question)
    legal_matches = sum(1 for keyword in legal_keywords if keyword in question)
    web_matches = sum(1 for keyword in web_search_keywords if keyword in question)
    
    # Route to the category with more matches
    # Web search has higher priority if explicitly requested
    if web_matches > 0 and web_matches >= max(order_matches, legal_matches):
        route = "web_search"
        needed_sources = ["web"]
        intent = "web_query"
        
    elif order_matches > legal_matches and order_matches > 0:
        route = "order_inquiry"
        needed_sources = ["mongo_db"]  # Orders are in MongoDB
        
        # Classify order-related intents
        if any(word in question for word in ["status", "track", "where"]):
            intent = "check_order_status"
        elif any(word in question for word in ["delivery", "arrive", "when"]):
            intent = "check_delivery_time"
        elif "cancel" in question:
            intent = "cancel_order"
        else:
            intent = "general_order_inquiry"
            
    elif legal_matches > 0:
        route = "legal_inquiry"
        needed_sources = ["vector_db"]  # Legal docs are in vector DB
        
        # Classify legal-related intents
        if any(word in question for word in ["privacy", "data", "gdpr"]):
            intent = "privacy_policy_query"
        elif any(word in question for word in ["terms", "tos", "agreement"]):
            intent = "terms_of_service_query"
        elif "refund" in question:
            intent = "refund_policy_query"
        else:
            intent = "general_legal_query"
    else:
        # General inquiry - might need both sources
        route = "general_inquiry"
        intent = "general_question"
        needed_sources = ["vector_db"]  # Default to vector DB for general questions
    
    result = {
        "route": route,
        "intent": intent,
        "needed_sources": needed_sources
    }
    
    # Stream metadata in custom mode
    try:
        writer = get_stream_writer()
        writer({"type": "metadata", "content": result})
    except Exception:
        pass # Fallback for non-streaming calls
        
    return result
