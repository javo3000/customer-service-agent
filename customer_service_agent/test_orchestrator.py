"""
Test script for orchestrator node.
Verifies keyword-based routing, intent classification, and state updates.
"""
import sys
sys.path.insert(0, 'src')

from agent.nodes.orchestrator import orchestrator


def test_order_inquiry():
    """Test order-related query routing."""
    state = {
        "question": "What is the status of my order?",
        "chat_history": [],
        "documents": [],
        "mongo_data": [],
        "final_answer": None,
        "feedback_score": None,
        "route": None,
        "intent": None,
        "needed_sources": []
    }
    
    result = orchestrator(state)
    
    assert result["route"] == "order_inquiry", f"Expected 'order_inquiry', got {result['route']}"
    assert result["intent"] == "check_order_status", f"Expected 'check_order_status', got {result['intent']}"
    assert "mongo_db" in result["needed_sources"], f"Expected 'mongo_db' in sources, got {result['needed_sources']}"
    
    print("✓ Order inquiry test passed")


def test_legal_inquiry():
    """Test legal/policy-related query routing."""
    state = {
        "question": "What is your privacy policy?",
        "chat_history": [],
        "documents": [],
        "mongo_data": [],
        "final_answer": None,
        "feedback_score": None,
        "route": None,
        "intent": None,
        "needed_sources": []
    }
    
    result = orchestrator(state)
    
    assert result["route"] == "legal_inquiry", f"Expected 'legal_inquiry', got {result['route']}"
    assert result["intent"] == "privacy_policy_query", f"Expected 'privacy_policy_query', got {result['intent']}"
    assert "vector_db" in result["needed_sources"], f"Expected 'vector_db' in sources, got {result['needed_sources']}"
    
    print("✓ Legal inquiry test passed")


def test_delivery_inquiry():
    """Test delivery time query routing."""
    state = {
        "question": "When will my package arrive?",
        "chat_history": [],
        "documents": [],
        "mongo_data": [],
        "final_answer": None,
        "feedback_score": None,
        "route": None,
        "intent": None,
        "needed_sources": []
    }
    
    result = orchestrator(state)
    
    assert result["route"] == "order_inquiry", f"Expected 'order_inquiry', got {result['route']}"
    assert result["intent"] == "check_delivery_time", f"Expected 'check_delivery_time', got {result['intent']}"
    assert "mongo_db" in result["needed_sources"], f"Expected 'mongo_db' in sources, got {result['needed_sources']}"
    
    print("✓ Delivery inquiry test passed")


def test_general_inquiry():
    """Test general query routing."""
    state = {
        "question": "How can I contact support?",
        "chat_history": [],
        "documents": [],
        "mongo_data": [],
        "final_answer": None,
        "feedback_score": None,
        "route": None,
        "intent": None,
        "needed_sources": []
    }
    
    result = orchestrator(state)
    
    assert result["route"] == "general_inquiry", f"Expected 'general_inquiry', got {result['route']}"
    assert result["intent"] == "general_question", f"Expected 'general_question', got {result['intent']}"
    assert "vector_db" in result["needed_sources"], f"Expected 'vector_db' in sources, got {result['needed_sources']}"
    
    print("✓ General inquiry test passed")


if __name__ == "__main__":
    print("Running orchestrator tests...\n")
    
    try:
        test_order_inquiry()
        test_legal_inquiry()
        test_delivery_inquiry()
        test_general_inquiry()
        
        print("\n✅ All tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
