"""
Unit tests for the RAG AI Agent module.

This module tests:
- OpenAI API integration with mocked responses
- Retrieval integration with known queries
- Grounding enforcement functions
- Error handling scenarios
- Response formatting and source attribution
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
# Add the backend directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.agent import (
    AgentQuery, AgentResponse, RAGAgent,
    create_rag_agent, query_agent,
    enforce_grounding, _retrieve_content,
    _format_sources
)
from backend.retrieve import RetrievalResult


class TestAgentModels(unittest.TestCase):
    """Test the data models for the agent."""

    def test_agent_query_creation(self):
        """Test AgentQuery model creation with default values."""
        query = AgentQuery(query_text="Test query")
        self.assertEqual(query.query_text, "Test query")
        self.assertEqual(query.max_results, 5)
        self.assertEqual(query.grounding_required, True)

    def test_agent_response_creation(self):
        """Test AgentResponse model creation."""
        response = AgentResponse(
            query="Test query",
            answer="Test answer",
            retrieved_context=[],
            sources=[],
            confidence=0.8
        )
        self.assertEqual(response.query, "Test query")
        self.assertEqual(response.answer, "Test answer")
        self.assertEqual(response.confidence, 0.8)

    def test_rag_agent_creation(self):
        """Test RAGAgent model creation."""
        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="Test prompt",
            retrieval_function=lambda x: []
        )
        self.assertEqual(agent.model_name, "gpt-4-turbo")
        self.assertEqual(agent.system_prompt, "Test prompt")
        self.assertEqual(agent.grounding_enforcement, True)


class TestCreateRagAgent(unittest.TestCase):
    """Test the RAG agent creation function."""

    def test_create_rag_agent_defaults(self):
        """Test creating a RAG agent with default parameters."""
        agent = create_rag_agent()
        self.assertEqual(agent.model_name, "gpt-4-turbo")
        self.assertTrue("helpful AI assistant" in agent.system_prompt)
        self.assertIsNotNone(agent.retrieval_function)

    def test_create_rag_agent_custom_model(self):
        """Test creating a RAG agent with custom model."""
        agent = create_rag_agent(model_name="gpt-3.5-turbo")
        self.assertEqual(agent.model_name, "gpt-3.5-turbo")


class TestRetrieveContent(unittest.TestCase):
    """Test the content retrieval function."""

    def test_retrieve_content_success(self):
        """Test successful content retrieval."""
        mock_retrieval_function = Mock()
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="Test content",
            metadata={"title": "Test", "url": "http://test.com"}
        )
        mock_retrieval_function.return_value = [mock_result]

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="Test",
            retrieval_function=mock_retrieval_function
        )

        results = _retrieve_content(agent, "test query", top_k=3)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].content, "Test content")
        mock_retrieval_function.assert_called_once_with("test query", top_k=3)

    def test_retrieve_content_error_handling(self):
        """Test content retrieval with error handling."""
        mock_retrieval_function = Mock()
        mock_retrieval_function.side_effect = Exception("Connection error")

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="Test",
            retrieval_function=mock_retrieval_function
        )

        results = _retrieve_content(agent, "test query")
        self.assertEqual(results, [])  # Should return empty list on error


class TestFormatSources(unittest.TestCase):
    """Test the source formatting function."""

    def test_format_sources_basic(self):
        """Test basic source formatting."""
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="Test content",
            metadata={"title": "Test Title", "url": "http://test.com"}
        )
        results = [mock_result]

        sources = _format_sources(results)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0], "Test Title (http://test.com)")

    def test_format_sources_duplicate_handling(self):
        """Test duplicate source handling."""
        mock_result1 = RetrievalResult(
            id="1",
            score=0.9,
            content="Test content 1",
            metadata={"title": "Test Title", "url": "http://test.com"}
        )
        mock_result2 = RetrievalResult(
            id="2",
            score=0.8,
            content="Test content 2",
            metadata={"title": "Test Title", "url": "http://test.com"}
        )
        results = [mock_result1, mock_result2]

        sources = _format_sources(results)
        self.assertEqual(len(sources), 1)  # Should only have one source despite two results
        self.assertEqual(sources[0], "Test Title (http://test.com)")

    def test_format_sources_missing_metadata(self):
        """Test source formatting with missing metadata."""
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="Test content",
            metadata={}
        )
        results = [mock_result]

        sources = _format_sources(results)
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0], "Unknown Title (No URL)")


class TestEnforceGrounding(unittest.TestCase):
    """Test the grounding enforcement function."""

    def test_grounding_with_context_overlap(self):
        """Test grounding enforcement with content overlap."""
        response_text = "This is a response based on the context."
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="This is the context for the response.",
            metadata={"title": "Test", "url": "http://test.com"}
        )
        retrieved_context = [mock_result]

        is_grounded = enforce_grounding(response_text, retrieved_context)
        self.assertTrue(is_grounded)

    def test_grounding_with_no_overlap(self):
        """Test grounding enforcement with no content overlap."""
        response_text = "This response has nothing to do with the context."
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="Completely different content here.",
            metadata={"title": "Test", "url": "http://test.com"}
        )
        retrieved_context = [mock_result]

        is_grounded = enforce_grounding(response_text, retrieved_context)
        # This might still return True if the response contains grounding phrases
        # Let's test with a response that has no overlap and no grounding phrases
        response_text = "Random response with no context connection at all."
        is_grounded = enforce_grounding(response_text, retrieved_context)
        self.assertFalse(is_grounded)

    def test_grounding_with_grounding_phrases(self):
        """Test grounding enforcement with grounding phrases."""
        response_text = "I cannot answer this based on the provided context."
        retrieved_context = []  # Empty context

        is_grounded = enforce_grounding(response_text, retrieved_context)
        self.assertTrue(is_grounded)  # Should be True because of the grounding phrase

    def test_grounding_with_empty_inputs(self):
        """Test grounding enforcement with empty inputs."""
        is_grounded = enforce_grounding("", [])
        self.assertFalse(is_grounded)

        is_grounded = enforce_grounding("Some response", [])
        self.assertFalse(is_grounded)

        is_grounded = enforce_grounding("", [RetrievalResult(
            id="1",
            score=0.9,
            content="Test",
            metadata={}
        )])
        self.assertFalse(is_grounded)


class TestQueryAgent(unittest.TestCase):
    """Test the main query agent function."""

    @patch('backend.agent.Runner')
    def test_query_agent_success(self, mock_runner):
        """Test successful query agent execution."""
        # Mock Agent response
        mock_result = MagicMock()
        mock_result.final_output = "This is the answer."
        mock_runner.run_sync.return_value = mock_result

        # Mock retrieval function
        mock_result_obj = RetrievalResult(
            id="1",
            score=0.9,
            content="Relevant content for the query.",
            metadata={"title": "Test Title", "url": "http://test.com"}
        )

        def mock_retrieval_function(query_text, top_k=5):
            return [mock_result_obj]

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="You are a helpful assistant.",
            retrieval_function=mock_retrieval_function
        )

        response = query_agent(agent, "Test query", top_k=3)

        self.assertEqual(response.query, "Test query")
        self.assertEqual(response.answer, "This is the answer.")
        self.assertEqual(len(response.retrieved_context), 1)
        self.assertEqual(len(response.sources), 1)
        self.assertGreater(response.confidence, 0)

    @patch('backend.agent.Runner')
    def test_query_agent_no_relevant_content(self, mock_runner):
        """Test query agent when no relevant content is found."""
        # Mock retrieval function to return empty results
        def mock_retrieval_function(query_text, top_k=5):
            return []

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="You are a helpful assistant.",
            retrieval_function=mock_retrieval_function
        )

        response = query_agent(agent, "Test query")

        self.assertEqual(response.query, "Test query")
        self.assertEqual(response.answer, "I cannot answer this question based on the provided context.")
        self.assertEqual(len(response.retrieved_context), 0)
        self.assertEqual(len(response.sources), 0)
        self.assertEqual(response.confidence, 0.0)

    @patch('backend.agent.Runner')
    def test_query_agent_api_error(self, mock_runner):
        """Test query agent when OpenAI Agents API call fails."""
        # Mock retrieval function
        mock_result = RetrievalResult(
            id="1",
            score=0.9,
            content="Relevant content.",
            metadata={"title": "Test", "url": "http://test.com"}
        )

        def mock_retrieval_function(query_text, top_k=5):
            return [mock_result]

        # Make Runner raise an exception
        mock_runner.run_sync.side_effect = Exception("API Error")

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="You are a helpful assistant.",
            retrieval_function=mock_retrieval_function
        )

        response = query_agent(agent, "Test query")

        self.assertEqual(response.query, "Test query")
        self.assertEqual(response.answer, "I encountered an error while processing your request. Please try again.")
        self.assertEqual(len(response.retrieved_context), 1)  # Retrieved content still there
        self.assertEqual(len(response.sources), 1)  # Sources still there
        self.assertEqual(response.confidence, 0.0)

    @patch('backend.agent.Runner')
    def test_query_agent_grounding_enforcement(self, mock_runner):
        """Test query agent with grounding enforcement."""
        # Mock Agent response
        mock_result = MagicMock()
        mock_result.final_output = "Response not grounded in context."
        mock_runner.run_sync.return_value = mock_result

        # Mock retrieval function
        mock_result_obj = RetrievalResult(
            id="1",
            score=0.9,
            content="Relevant content for the query.",
            metadata={"title": "Test Title", "url": "http://test.com"}
        )

        def mock_retrieval_function(query_text, top_k=5):
            return [mock_result_obj]

        agent = RAGAgent(
            model_name="gpt-4-turbo",
            system_prompt="You are a helpful assistant.",
            retrieval_function=mock_retrieval_function,
            grounding_enforcement=True  # Enable grounding enforcement
        )

        response = query_agent(agent, "Test query")

        # Should return a response indicating the grounding issue
        self.assertIn("may not be fully grounded", response.answer)
        self.assertEqual(response.confidence, 0.0)


if __name__ == '__main__':
    unittest.main()