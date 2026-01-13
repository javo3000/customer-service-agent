import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import app as main_app

def create_dev_app():
    # Enable debug mode
    # Note: FastAPI doesn't have a global debug flag like Flask, 
    # but we can configure things here if needed.
    
    # Add CORS middleware for development
    main_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add health check endpoint
    @main_app.get("/health")
    async def health_check():
        return {"status": "ok", "environment": "development"}
        
    return main_app

if __name__ == "__main__":
    # Configure uvicorn
    uvicorn.run(
        "development:create_dev_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        factory=True
    )
