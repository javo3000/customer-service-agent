"""
Test script for the full graph workflow.
Verifies end-to-end execution of the customer service agent.
"""
import sys
sys.path.insert(0, 'src')

from unittest.mock import patch
from agent.graph import graph


def test_order_workflow():
    """Test end-to-end order inquiry workflow."""
    print("\n--- Testing Order Workflow ---")
    
    # Mock the tool call to avoid actual DB connection
    # Mock the tool call to avoid actual DB connection
    # We need to patch where it's imported in the tool_node module
    with patch('src.agent.nodes.tool_node.query_order_tool') as mock_tool:
        mock_tool.return_value = "Order Found:\nID: ORD123\nStatus: Delivered\nItems: Laptop\nTotal: $999.00"
        
        initial_state = {
            "question": "What is the status of order ORD123?",
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None
        }
        
        # Invoke the graph
        result = graph.invoke(initial_state)
        
        # Verify routing
        assert result["route"] == "order_inquiry"
        assert result["intent"] == "check_order_status"
        assert "mongo_db" in result["needed_sources"]
        
        # Verify tool execution
        assert len(result["mongo_data"]) > 0
        assert result["mongo_data"][0]["order_id"] == "ORD123"
        
        # Verify final answer
        answer = result["final_answer"]
        print(f"Final Answer:\n{answer}")
        
        assert "Dear Valued Client" in answer
        assert "ORD123" in answer
        assert "Delivered" in answer
        
        print("✓ Order workflow passed")


def test_legal_workflow():
    """Test end-to-end legal inquiry workflow."""
    print("\n--- Testing Legal Workflow ---")
    
    # Mock the tool call
    # Mock the tool call
    with patch('src.agent.nodes.tool_node.search_legal_docs_tool') as mock_tool:
        mock_tool.return_value = "We value your privacy. Data is encrypted at rest."
        
        initial_state = {
            "question": "What is your privacy policy?",
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None
        }
        
        # Invoke the graph
        result = graph.invoke(initial_state)
        
        # Verify routing
        assert result["route"] == "legal_inquiry"
        assert result["intent"] == "privacy_policy_query"
        assert "vector_db" in result["needed_sources"]
        
        # Verify tool execution
        assert len(result["documents"]) > 0
        
        # Verify final answer
        answer = result["final_answer"]
        print(f"Final Answer:\n{answer}")
        
        assert "Dear Valued Client" in answer
        assert "privacy" in answer.lower()
        assert "Citation:" in answer
        
        print("✓ Legal workflow passed")


def test_general_workflow():
    """Test end-to-end general inquiry workflow."""
    print("\n--- Testing General Workflow ---")
    
    # Mock both tools
    # Mock both tools
    with patch('src.agent.nodes.tool_node.search_legal_docs_tool') as mock_search:
        mock_search.return_value = "Support is available 24/7."
        
        initial_state = {
            "question": "How can I contact support?",
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None
        }
        
        # Invoke the graph
        result = graph.invoke(initial_state)
        
        # Verify routing
        assert result["route"] == "general_inquiry"
        
        # Verify final answer
        answer = result["final_answer"]
        print(f"Final Answer:\n{answer}")
        
        assert "Dear Valued Client" in answer
        assert "Support" in answer
        
        print("✓ General workflow passed")


if __name__ == "__main__":
    print("Running full workflow tests...")
    
    try:
        test_order_workflow()
        test_legal_workflow()
        test_general_workflow()
        
        print("\n✅ All workflow tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
