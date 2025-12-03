"""
Orchestrator node for routing customer service queries.
Performs keyword-based routing and intent classification.
"""
from typing import Dict, List
from src.agent.state import AgentState


def orchestrator(state: AgentState) -> Dict:
    """
    Routes queries based on keyword matching and updates state with:
    - route: 'order_inquiry' or 'legal_inquiry'
    - intent: classified intent
    - needed_sources: list of required data sources
    
    Args:
        state: Current agent state with user question
        
    Returns:
        Dictionary with route, intent, and needed_sources updates
    """
    question = state.get("question", "").lower()
    
    # Keyword sets for routing
    order_keywords = {
        "order", "status", "shipping", "delivery", "track", "package",
        "shipment", "tracking", "delivered", "ship", "arrive", "when"
    }
    
    legal_keywords = {
        "legal", "terms", "privacy", "policy", "policies", "agreement",
        "terms of service", "tos", "gdpr", "data", "rights", "refund policy"
    }
    
    # Determine route based on keyword presence
    route = "general_inquiry"  # default
    intent = "unknown"
    needed_sources = []
    
    # Count keyword matches
    order_matches = sum(1 for keyword in order_keywords if keyword in question)
    legal_matches = sum(1 for keyword in legal_keywords if keyword in question)
    
    # Route to the category with more matches
    if order_matches > legal_matches and order_matches > 0:
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
    
    return {
        "route": route,
        "intent": intent,
        "needed_sources": needed_sources
    }
