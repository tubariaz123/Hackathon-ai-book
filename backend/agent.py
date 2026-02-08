"""
RAG AI Agent with OpenAI Agents SDK and Qdrant integration.

This module provides functionality for:
- Creating a RAG (Retrieval-Augmented Generation) agent using OpenAI Agents SDK
- Integrating with existing Qdrant search functionality
- Enforcing strict grounding in retrieved content
"""
import os
import logging
import time
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import sys
import os
import warnings

# Suppress the deprecation warning before importing the module
warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

import google.generativeai as genai

# Configure Google GenAI with the provided API key
GEMINI_API_KEY = "AIzaSyA08apsET3nibiGbVb0D-rl78h99SqcG5s"
genai.configure(api_key=GEMINI_API_KEY)

# Select the Gemini model
model = genai.GenerativeModel('gemini-2.5-flash')


# Add the backend directory to the path so we can import from it when run from project root
sys.path.insert(0, os.path.dirname(__file__))

from retrieve import search_similar_content, RetrievalResult

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# Data Models
@dataclass
class AgentQuery:
    """Data model for an agent query."""
    query_text: str
    max_results: int = 5
    grounding_required: bool = True


@dataclass
class AgentResponse:
    """Data model for an agent response."""
    query: str
    answer: str
    retrieved_context: List[RetrievalResult]
    sources: List[str]
    confidence: float = 0.0


@dataclass
class RAGAgent:
    """Data model for the RAG agent."""
    model_name: str
    system_prompt: str
    retrieval_function: Callable
    grounding_enforcement: bool = False


def create_rag_agent(model_name: str = "gpt-3.5-turbo") -> RAGAgent:
    """
    Initialize and return a RAG agent with specified OpenAI model.

    Args:
        model_name: The OpenAI model to use (default: "gpt-3.5-turbo")

    Returns:
        RAGAgent object configured for grounded responses
    """
    system_prompt = """You are a helpful AI assistant that answers questions based only on the provided context.
    Do not use any prior knowledge or information not included in the provided context.
    If the context does not contain information to answer the question, respond with:
    "I cannot answer this question based on the provided context."
    Always cite your sources when providing answers."""

    return RAGAgent(
        model_name=model_name,
        system_prompt=system_prompt,
        retrieval_function=search_similar_content,
        grounding_enforcement=True
    )


def _retrieve_content(agent: RAGAgent, query_text: str, top_k: int = 5) -> List[RetrievalResult]:
    """
    Wrapper function to handle retrieval with proper error handling.

    Args:
        agent: The RAG agent with retrieval function
        query_text: The query text to search for
        top_k: Number of results to retrieve

    Returns:
        List of RetrievalResult objects
    """
    try:
        logger.info(f"Starting content retrieval for query: '{query_text[:50]}...'")
        results = agent.retrieval_function(query_text, top_k=top_k)
        logger.info(f"Retrieved {len(results)} results from Qdrant")
        return results
    except Exception as e:
        logger.error(f"Error during content retrieval: {str(e)}")
        return []


def _format_sources(retrieved_results: List[RetrievalResult]) -> List[str]:
    """
    Format retrieved results to include source information from metadata.

    Args:
        retrieved_results: List of retrieved results

    Returns:
        List of source identifiers
    """
    sources = []
    for result in retrieved_results:
        # Extract source information from metadata
        source_title = result.metadata.get('title', 'Unknown Title')
        source_url = result.metadata.get('url', 'No URL')
        source = f"{source_title} ({source_url})"
        if source not in sources:  # Avoid duplicates
            sources.append(source)
    return sources


def query_agent(agent: RAGAgent, query_text: str, top_k: int = 5) -> AgentResponse:
    """
    Process a user query through the RAG agent.

    Args:
        agent: The configured RAG agent
        query_text: The user's question
        top_k: Number of results to retrieve from Qdrant

    Returns:
        AgentResponse object with answer and source information
    """
    logger.info(f"Processing query through RAG agent: '{query_text[:50]}...'")

    # Retrieve relevant content using the integrated search function
    retrieved_results = _retrieve_content(agent, query_text, top_k)

    if not retrieved_results:
        logger.warning(f"No relevant content found for query: '{query_text[:50]}...'")
        return AgentResponse(
            query=query_text,
            answer="I cannot answer this question based on the provided context.",
            retrieved_context=[],
            sources=[],
            confidence=0.0
        )

    # Format retrieved context for use with OpenAI Agents SDK
    context_text = "\n\n".join([
        f"Source {i+1}: {result.content}"
        for i, result in enumerate(retrieved_results)
    ])

    # Prepare the full context for the agent
    full_context = f"Context:\n{context_text}\n\nQuestion: {query_text}"

    try:
        # Use Google Gemini API to generate response with the context and system prompt
        # Combine system prompt and user query
        combined_prompt = f"{agent.system_prompt}\n\n{full_context}"

        response = model.generate_content(
            combined_prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )

        answer = response.text

        # Calculate a basic confidence score based on the number and relevance of retrieved results
        avg_score = sum(result.score for result in retrieved_results) / len(retrieved_results) if retrieved_results else 0.0
        confidence = min(1.0, avg_score / 2.0)  # Normalize the score to 0-1 range

        # Format sources
        sources = _format_sources(retrieved_results)

        logger.info(f"Successfully generated answer for query: '{query_text[:50]}...'")

        # If grounding enforcement is required, validate the response
        if agent.grounding_enforcement:
            is_grounded = enforce_grounding(answer, retrieved_results)
            if not is_grounded:
                logger.warning(f"Response not properly grounded for query: '{query_text[:50]}...'")
                return AgentResponse(
                    query=query_text,
                    answer="I cannot answer this question based on the provided context. The response may not be fully grounded in the retrieved content.",
                    retrieved_context=retrieved_results,
                    sources=sources,
                    confidence=0.0
                )

        # Create and return properly formatted AgentResponse
        return AgentResponse(
            query=query_text,
            answer=answer,
            retrieved_context=retrieved_results,
            sources=sources,
            confidence=confidence
        )

    except Exception as e:
        # Handle specific Gemini API errors
        error_message = str(e).lower()
        if "404" in error_message and "model" in error_message:
            logger.error(f"Gemini model not found or accessible: {str(e)}")
            return AgentResponse(
                query=query_text,
                answer="The AI model is currently not accessible. Please check the API configuration and model availability.",
                retrieved_context=retrieved_results,
                sources=_format_sources(retrieved_results),
                confidence=0.0
            )
        elif "api" in error_message or "key" in error_message or "auth" in error_message:
            logger.error(f"Gemini API authentication or authorization error: {str(e)}")
            return AgentResponse(
                query=query_text,
                answer="There is an issue with the API key or authentication. Please verify the Google Gemini API configuration.",
                retrieved_context=retrieved_results,
                sources=_format_sources(retrieved_results),
                confidence=0.0
            )
        else:
            # For other errors, fall back to the original error handling
            logger.error(f"Error generating response: {str(e)}")
            return AgentResponse(
                query=query_text,
                answer="I encountered an error while processing your request. Please try again.",
                retrieved_context=retrieved_results,
                sources=_format_sources(retrieved_results),
                confidence=0.0
            )


def enforce_grounding(response_text: str, retrieved_context: List[RetrievalResult]) -> bool:
    """
    Validate that the response is grounded in retrieved context.

    Args:
        response_text: The generated response
        retrieved_context: Retrieved content used for response

    Returns:
        Boolean indicating if response is properly grounded
    """
    if not response_text:
        return False

    # Convert to lowercase for comparison
    response_lower = response_text.lower()

    # Additional check: see if response contains phrases that indicate it's citing sources
    # or acknowledging limitations of the provided context - this should be checked first
    non_committal_phrases = [
        "i cannot answer",
        "no relevant context",
        "not in the provided context",
        "based on the provided context",
        "according to the context"
    ]

    for phrase in non_committal_phrases:
        if phrase in response_lower:
            return True  # These phrases indicate proper grounding behavior

    # If there's no retrieved context, and no grounding phrases, it's not grounded
    if not retrieved_context:
        return False

    # Check if the response references content from the retrieved context
    for result in retrieved_context:
        content_lower = result.content.lower()

        # Simple check: see if there's significant overlap between response and context
        # Split into words
        response_words = set(response_lower.split())
        content_words = set(content_lower.split())

        # Calculate intersection
        intersection = response_words.intersection(content_words)

        # If there's meaningful overlap, consider it grounded
        if len(intersection) > 0:
            # Calculate a simple ratio of overlap
            overlap_ratio = len(intersection) / len(response_words) if response_words else 0
            if overlap_ratio > 0.1:  # At least 10% of response words appear in context
                return True

    return False  # No significant overlap found


if __name__ == "__main__":

    agent = create_rag_agent()

    query = "What is ROS 2?"

    response = query_agent(agent, query)

    print("\n===== FINAL ANSWER =====\n")
    print(response.answer)

    print("\n===== SOURCES =====")
    for src in response.sources:
        print("-", src)


