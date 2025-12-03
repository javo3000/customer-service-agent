"""
Test script for generate node.
Verifies context preparation and error handling with mocked LLM.
"""
import sys
import unittest
from unittest.mock import MagicMock, patch
sys.path.insert(0, 'src')

from langchain_core.documents import Document
from src.agent.nodes.generate import generate, _prepare_context

class TestGenerateNode(unittest.TestCase):
    
    def setUp(self):
        # Mock the chain to avoid real API calls
        self.patcher = patch('src.agent.nodes.generate.chain')
        self.mock_chain = self.patcher.start()
        
    def tearDown(self):
        self.patcher.stop()

    def test_prepare_context_order(self):
        """Test context preparation with order data."""
        mongo_data = [{
            "order_id": "ABC123",
            "result": "Order Found:\nID: ABC123\nStatus: Shipped",
            "success": True
        }]
        documents = []
        
        context = _prepare_context(mongo_data, documents)
        
        self.assertIn("ORDER DATA:", context)
        self.assertIn("ID: ABC123", context)
        self.assertIn("Status: Shipped", context)

    def test_prepare_context_legal(self):
        """Test context preparation with legal documents."""
        mongo_data = []
        documents = [
            Document(
                page_content="We collect personal data.",
                metadata={"source": "Privacy Policy"}
            )
        ]
        
        context = _prepare_context(mongo_data, documents)
        
        self.assertIn("POLICY DOCUMENTS:", context)
        self.assertIn("We collect personal data.", context)
        self.assertIn("Source: Privacy Policy", context)

    def test_prepare_context_fusion(self):
        """Test context preparation with both data sources."""
        mongo_data = [{"result": "Order Info"}]
        documents = [Document(page_content="Policy Info")]
        
        context = _prepare_context(mongo_data, documents)
        
        self.assertIn("ORDER DATA:", context)
        self.assertIn("Order Info", context)
        self.assertIn("POLICY DOCUMENTS:", context)
        self.assertIn("Policy Info", context)

    def test_generate_success(self):
        """Test successful generation flow."""
        state = {
            "question": "Status?",
            "mongo_data": [{"result": "Order Info"}],
            "documents": []
        }
        
        # Mock LLM response
        self.mock_chain.invoke.return_value = "Dear Client, Your order is shipped."
        
        result = generate(state)
        
        # Verify chain was called with correct context
        args = self.mock_chain.invoke.call_args[0][0]
        self.assertIn("ORDER DATA:", args["context"])
        self.assertIn("Status?", args["question"])
        
        # Verify result
        self.assertEqual(result["final_answer"], "Dear Client, Your order is shipped.")

    def test_generate_error_handling(self):
        """Test error handling when LLM fails."""
        state = {"question": "Status?"}
        
        # Mock LLM error
        self.mock_chain.invoke.side_effect = Exception("API Error")
        
        result = generate(state)
        
        self.assertIn("regret to inform you", result["final_answer"])
        self.assertIn("technical issue", result["final_answer"])

if __name__ == "__main__":
    unittest.main()
