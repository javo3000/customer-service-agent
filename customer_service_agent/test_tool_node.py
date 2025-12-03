"""
Test script for tool_node.
Verifies conditional tool execution, parameter extraction, and error handling.
"""
import sys
sys.path.insert(0, 'src')

from unittest.mock import patch, MagicMock
from langchain_core.documents import Document

from agent.nodes.tool_node import tool_node, extract_order_id


def test_extract_order_id():
    """Test order ID extraction from various question formats."""
    test_cases = [
        ("What is the status of order ABC123?", "ABC123"),
        ("Track my order: XYZ789", "XYZ789"),
        ("Where is order #ORDER-456?", "ORDER-456"),
        ("My order number is 123456", "123456"),
        ("Status of ORD999", "ORD999"),
    ]
    
    for question, expected in test_cases:
        result = extract_order_id(question)
        assert result == expected, f"Failed for '{question}': expected '{expected}', got '{result}'"
    
    print("✓ Order ID extraction tests passed")


def test_mongo_tool_execution():
    """Test MongoDB tool execution path."""
    
    with patch('agent.nodes.tool_node.query_order_tool') as mock_tool:
        mock_tool.return_value = "Order Found:\nID: ABC123\nStatus: Shipped"
        
        state = {
            "question": "What is the status of order ABC123?",
            "needed_sources": ["mongo_db"],
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None,
            "route": "order_inquiry",
            "intent": "check_order_status"
        }
        
        result = tool_node(state)
        
        # Verify tool was called
        mock_tool.assert_called_once_with("ABC123")
        
        # Verify state updates
        assert "mongo_data" in result
        assert len(result["mongo_data"]) == 1
        assert result["mongo_data"][0]["order_id"] == "ABC123"
        assert result["mongo_data"][0]["success"] is True
        
        print("✓ MongoDB tool execution test passed")


def test_vector_tool_execution():
    """Test Vector DB tool execution path."""
    
    with patch('agent.nodes.tool_node.search_legal_docs_tool') as mock_tool:
        mock_tool.return_value = "Found: Privacy policy information..."
        
        state = {
            "question": "What is your privacy policy?",
            "needed_sources": ["vector_db"],
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None,
            "route": "legal_inquiry",
            "intent": "privacy_policy_query"
        }
        
        result = tool_node(state)
        
        # Verify tool was called
        mock_tool.assert_called_once_with("What is your privacy policy?")
        
        # Verify state updates
        assert "documents" in result
        assert len(result["documents"]) == 1
        assert isinstance(result["documents"][0], Document)
        assert "Privacy policy" in result["documents"][0].page_content
        
        print("✓ Vector DB tool execution test passed")


def test_error_handling_mongo():
    """Test error handling for MongoDB tool failures."""
    
    with patch('agent.nodes.tool_node.query_order_tool') as mock_tool:
        mock_tool.side_effect = Exception("Database connection failed")
        
        state = {
            "question": "What is the status of order ABC123?",
            "needed_sources": ["mongo_db"],
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None,
            "route": "order_inquiry",
            "intent": "check_order_status"
        }
        
        result = tool_node(state)
        
        # Verify error handling
        assert "mongo_data" in result
        assert "error" in result["mongo_data"][0]
        assert "Database connection failed" in result["mongo_data"][0]["error"]
        
        print("✓ MongoDB error handling test passed")


def test_no_order_id_extraction():
    """Test handling when order ID cannot be extracted."""
    
    with patch('agent.nodes.tool_node.query_order_tool') as mock_tool:
        state = {
            "question": "I have a problem with my order",  # No order ID
            "needed_sources": ["mongo_db"],
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None,
            "route": "order_inquiry",
            "intent": "general_order_inquiry"
        }
        
        result = tool_node(state)
        
        # Tool should not be called if no order ID
        mock_tool.assert_not_called()
        
        # Should have error message
        assert "mongo_data" in result
        assert "error" in result["mongo_data"][0]
        assert "Could not extract order ID" in result["mongo_data"][0]["error"]
        
        print("✓ No order ID extraction test passed")


def test_multiple_sources():
    """Test execution with multiple needed sources."""
    
    with patch('agent.nodes.tool_node.query_order_tool') as mock_order, \
         patch('agent.nodes.tool_node.search_legal_docs_tool') as mock_search:
        
        mock_order.return_value = "Order Found"
        mock_search.return_value = "Search Results"
        
        state = {
            "question": "What is the status of order ABC123 and what is your refund policy?",
            "needed_sources": ["mongo_db", "vector_db"],
            "chat_history": [],
            "documents": [],
            "mongo_data": [],
            "final_answer": None,
            "feedback_score": None,
            "route": "general_inquiry",
            "intent": "complex_query"
        }
        
        result = tool_node(state)
        
        # Both tools should be called
        mock_order.assert_called_once()
        mock_search.assert_called_once()
        
        # Both data types should be updated
        assert "mongo_data" in result
        assert "documents" in result
        
        print("✓ Multiple sources test passed")


if __name__ == "__main__":
    print("Running tool_node tests...\n")
    
    try:
        test_extract_order_id()
        test_mongo_tool_execution()
        test_vector_tool_execution()
        test_error_handling_mongo()
        test_no_order_id_extraction()
        test_multiple_sources()
        
        print("\n✅ All tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
