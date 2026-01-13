"""
FastAPI application for the Customer Service Agent.
Exposes an /ask endpoint to interact with the agent graph.
"""
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from langfuse.callback import CallbackHandler
from src.agent.graph import graph
from src.config import settings

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

from fastapi.responses import StreamingResponse
import json

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    """
    Process a user query through the agent graph with real-time streaming results.
    """
    async def event_generator():
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
            
            # Initialize Langfuse CallbackHandler
            langfuse_handler = CallbackHandler(
                secret_key=settings.LANGFUSE_SECRET_KEY.get_secret_value() if settings.LANGFUSE_SECRET_KEY else None,
                public_key=settings.LANGFUSE_PUBLIC_KEY,
                host=settings.LANGFUSE_HOST
            )

            # Use graph.astream with stream_mode="custom"
            async for chunk in graph.astream(
                initial_state,
                stream_mode="custom",
                config={"callbacks": [langfuse_handler]}
            ):
                # 'chunk' is exactly what we passed to writer() in the nodes
                yield f"data: {json.dumps(chunk)}\n\n"

        except Exception as e:
            logger.error(f"Error in stream: {e}")
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # Use string "main:app" and reload=True to enable auto-reload
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
