"""
Test script for the FastAPI application.
Verifies the /ask endpoint and error handling.
"""
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the app (will fail if main.py is not implemented yet, but that's TDD)
# We'll need to make sure main.py exists with at least the app object for this to import
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint to ensure API is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_ask_endpoint_success():
    """Test the /ask endpoint with a valid query."""
    
    # Mock the graph invocation
    mock_response = {
        "final_answer": "Dear Valued Client,\n\nYour order is shipped.",
        "route": "order_inquiry",
        "needed_sources": ["mongo_db"]
    }
    
    with patch('src.agent.graph.graph.invoke') as mock_invoke:
        mock_invoke.return_value = mock_response
        
        payload = {
            "question": "What is the status of order 123?",
            "chat_history": []
        }
        
        response = client.post("/ask", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["answer"] == mock_response["final_answer"]
        assert data["route"] == mock_response["route"]
        assert data["sources"] == mock_response["needed_sources"]
        
        # Verify graph was called with correct state
        mock_invoke.assert_called_once()
        call_args = mock_invoke.call_args[0][0]
        assert call_args["question"] == payload["question"]

def test_ask_endpoint_validation_error():
    """Test validation error for missing required fields."""
    payload = {
        "chat_history": []
        # Missing 'question'
    }
    
    response = client.post("/ask", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_ask_endpoint_internal_error():
    """Test handling of internal errors during graph execution."""
    
    with patch('src.agent.graph.graph.invoke') as mock_invoke:
        mock_invoke.side_effect = Exception("Graph execution failed")
        
        payload = {
            "question": "Trigger error"
        }
        
        response = client.post("/ask", json=payload)
        
        assert response.status_code == 500
        assert "detail" in response.json()

if __name__ == "__main__":
    # Manually run tests if executed as script
    try:
        test_root_endpoint()
        print("✓ Root endpoint test passed")
        
        test_ask_endpoint_success()
        print("✓ Ask endpoint success test passed")
        
        test_ask_endpoint_validation_error()
        print("✓ Validation error test passed")
        
        test_ask_endpoint_internal_error()
        print("✓ Internal error test passed")
        
        print("\n✅ All API tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
