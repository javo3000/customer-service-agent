from typing import TypedDict, Annotated, List, Optional, Union, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document

class AgentState(TypedDict):
    """
    Represents the state of the customer service agent.
    """
    # The user's original question
    question: str
    
    # Chat history (persisted across turns)
    # add_messages reducer handles appending new messages to the list
    chat_history: Annotated[List[BaseMessage], add_messages]
    
    # Retrieved documents from Vector DB
    documents: List[Document]
    
    # Data retrieved from MongoDB (e.g., customer info, order status)
    mongo_data: List[dict]
    
    # The final generated answer to send back to the user
    final_answer: Optional[str]
    
    # Optional feedback score from the user (0.0 to 1.0)
    feedback_score: Optional[float]
    
    # Route determined by the orchestrator ('order_inquiry', 'legal_inquiry', etc.)
    route: Optional[str]
    
    # Classified intent (e.g., 'check_status', 'policy_query')
    intent: Optional[str]
    
    # Data sources needed for this query (e.g., ['vector_db', 'mongo_db'])
    needed_sources: List[str]

def validate_state(state: AgentState, required_fields: List[str]) -> bool:
    """
    Validates that the state contains the required fields.
    Raises ValueError if a field is missing.
    """
    missing = []
    for field in required_fields:
        if field not in state or state[field] is None:
            missing.append(field)
        elif isinstance(state[field], str) and not state[field].strip():
            # Also treat empty or whitespace-only strings as missing
            missing.append(field)
    
    if missing:
        raise ValueError(f"State is missing required fields: {', '.join(missing)}")
    
    return True
