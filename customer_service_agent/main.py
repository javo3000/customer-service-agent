"""
FastAPI application for the Customer Service Agent.
Exposes an /ask endpoint to interact with the agent graph.
"""
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agent.graph import graph

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Service Agent",
    description="A formal tax advisory customer service agent",
    version="1.0.0"
)

# --- Pydantic Models ---

class QueryRequest(BaseModel):
    """Request model for the /ask endpoint."""
    question: str = Field(..., description="The user's question")
    chat_history: Optional[List[Dict[str, str]]] = Field(
        default=[], 
        description="Previous chat history (optional)"
    )

class QueryResponse(BaseModel):
    """Response model for the /ask endpoint."""
    answer: str = Field(..., description="The agent's final answer")
    route: str = Field(..., description="The routing decision made")
    sources: List[str] = Field(..., description="Data sources used")

# --- Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Customer Service Agent is running"}

@app.post("/ask", response_model=QueryResponse)
async def ask_agent(request: QueryRequest):
    """
    Process a user query through the agent graph.
    
    Args:
        request: QueryRequest containing the question
        
    Returns:
        QueryResponse with the answer and metadata
    """
    try:
        logger.info(f"Received query: {request.question}")
        
        # Initialize state
        initial_state = {
            "question": request.question,
            "chat_history": request.chat_history,
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None
        }
        
        # Invoke the graph
        result = graph.invoke(initial_state)
        
        # Extract results
        final_answer = result.get("final_answer", "No answer generated.")
        route = result.get("route", "unknown")
        needed_sources = result.get("needed_sources", [])
        
        logger.info(f"Query processed. Route: {route}")
        
        return QueryResponse(
            answer=final_answer,
            route=route,
            sources=needed_sources
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
