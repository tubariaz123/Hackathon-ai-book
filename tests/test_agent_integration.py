"""
Integration tests for the RAG AI Agent module.

This module tests:
- End-to-end RAG functionality with real OpenAI and Qdrant connection
- Response grounding validation in real scenarios
- Source attribution and metadata handling
- Grounding enforcement functionality
"""
import unittest
import os
from dotenv import load_dotenv
from backend.agent import (
    create_rag_agent, query_agent,
    AgentResponse
)
from backend.retrieve import search_similar_content


# Load environment variables for integration tests
load_dotenv()


class TestAgentIntegration(unittest.TestCase):
    """Integration tests for the RAG AI Agent."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment for integration tests."""
        # Check if required environment variables are available
        cls.openai_api_key = os.getenv("OPENAI_API_KEY")
        cls.qdrant_url = os.getenv("QDRANT_URL")
        cls.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not all([cls.openai_api_key, cls.qdrant_url, cls.qdrant_api_key]):
            raise unittest.SkipTest("Required environment variables not set for integration tests")

    def test_end_to_end_rag_functionality(self):
        """Test end-to-end RAG functionality with real OpenAI and Qdrant connection."""
        # Create a RAG agent
        agent = create_rag_agent(model_name="gpt-3.5-turbo")

        # Test with a simple query
        query_text = "What is artificial intelligence?"

        # Process the query through the agent
        response = query_agent(agent, query_text, top_k=3)

        # Validate the response structure
        self.assertIsInstance(response, AgentResponse)
        self.assertEqual(response.query, query_text)
        self.assertIsInstance(response.answer, str)
        self.assertIsInstance(response.retrieved_context, list)
        self.assertIsInstance(response.sources, list)
        self.assertIsInstance(response.confidence, float)
        self.assertGreaterEqual(response.confidence, 0.0)
        self.assertLessEqual(response.confidence, 1.0)

        # Validate that sources are properly attributed when context exists
        if response.retrieved_context:
            self.assertGreater(len(response.sources), 0,
                              "Sources should be populated when context is retrieved")

    def test_response_grounding_in_retrieved_context(self):
        """Test that responses are grounded in retrieved context."""
        agent = create_rag_agent(model_name="gpt-3.5-turbo")

        # Use a specific query that should have relevant content in Qdrant
        query_text = "What are the key principles of machine learning?"

        response = query_agent(agent, query_text, top_k=5)

        # The response should be based on the retrieved context
        # Check that the answer is meaningful and not a generic response
        self.assertGreater(len(response.answer.strip()), 0,
                          "Response should contain an answer")
        self.assertNotIn("I cannot answer", response.answer,
                         "Response should not indicate inability to answer if context exists")

        # If context was retrieved, verify that sources are provided
        if response.retrieved_context:
            self.assertGreater(len(response.sources), 0,
                              "Sources should be provided when context is retrieved")
            # Check that the confidence is reasonably high when context exists
            self.assertGreater(response.confidence, 0.0,
                              "Confidence should be greater than 0 when context exists")

    def test_source_attribution_and_metadata_handling(self):
        """Test source attribution and metadata handling."""
        agent = create_rag_agent(model_name="gpt-3.5-turbo")

        # Query that should return results
        query_text = "AI development"

        response = query_agent(agent, query_text, top_k=2)

        # Verify that sources contain proper attribution
        for source in response.sources:
            # Sources should contain both title and URL information
            self.assertIsInstance(source, str)
            # Source should contain a URL in parentheses
            self.assertIn("(", source)
            self.assertIn(")", source)

        # Verify that retrieved context has proper metadata
        for result in response.retrieved_context:
            self.assertIsNotNone(result.metadata)
            # Should have at least title and URL in metadata
            self.assertIn('title', result.metadata)
            self.assertIn('url', result.metadata)

    def test_grounding_enforcement_functionality(self):
        """Test grounding enforcement functionality."""
        # Create agent with grounding enforcement enabled (default)
        agent = create_rag_agent(model_name="gpt-3.5-turbo")

        # Test with a query that might not have relevant context
        # Use a very specific or obscure query
        obscure_query = "What is the meaning of xyzabc123 in AI research?"

        response = query_agent(agent, obscure_query, top_k=1)

        # First, check if any relevant context was found
        if not response.retrieved_context:
            # If no context found, the agent should indicate this
            self.assertIn("cannot answer", response.answer.lower())
        else:
            # If context was found, the answer should be grounded in that context
            self.assertGreater(len(response.answer), 0)
            # The answer should reference the provided context in some way
            self.assertNotIn("I don't know", response.answer,
                             "Grounded responses should not say 'I don't know'")

    def test_agent_with_different_models(self):
        """Test agent functionality with different OpenAI models."""
        models_to_test = ["gpt-3.5-turbo"]

        # Only test gpt-4-turbo if it's available in the environment
        if os.getenv("TEST_GPT4", "").lower() == "true":
            models_to_test.append("gpt-4-turbo")

        query_text = "What is Python programming?"

        for model in models_to_test:
            with self.subTest(model=model):
                agent = create_rag_agent(model_name=model)
                response = query_agent(agent, query_text, top_k=2)

                # Validate response structure for each model
                self.assertIsInstance(response, AgentResponse)
                self.assertEqual(response.query, query_text)
                self.assertGreater(len(response.answer), 0)

    def test_agent_with_various_query_types(self):
        """Test agent with different types of queries."""
        agent = create_rag_agent(model_name="gpt-3.5-turbo")

        test_queries = [
            "What is AI?",  # Short query
            "Explain the principles of machine learning in detail",  # Long query
            "Python programming language",  # General topic
        ]

        for query in test_queries:
            with self.subTest(query=query):
                response = query_agent(agent, query, top_k=3)

                # Validate response for each query type
                self.assertIsInstance(response, AgentResponse)
                self.assertEqual(response.query, query)
                # Response should be meaningful
                self.assertGreater(len(response.answer.strip()), 0)


def run_integration_tests():
    """Helper function to run the integration tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAgentIntegration)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == '__main__':
    # Check if environment variables are available before running tests
    if not all([os.getenv("OPENAI_API_KEY"), os.getenv("QDRANT_URL"), os.getenv("QDRANT_API_KEY")]):
        print("Environment variables for integration tests not set.")
        print("Please set OPENAI_API_KEY, QDRANT_URL, and QDRANT_API_KEY to run integration tests.")
        exit(1)

    unittest.main()