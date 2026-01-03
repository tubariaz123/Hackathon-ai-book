"""
Retrieval and pipeline validation module.

This module provides functionality for:
- Semantic similarity search against Qdrant collection
- Retrieval pipeline validation
- Result relevance and stability verification
"""

import os
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")
qdrant_client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=60.0,  # Set timeout to 60 seconds
)


@dataclass
class Query:
    """Data model for a search query."""
    query_text: str
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None


@dataclass
class RetrievalResult:
    """Data model for a retrieval result."""
    id: str
    score: float
    content: str
    metadata: Dict[str, Any]
    relevance: Optional[float] = None


@dataclass
class ValidationResult:
    """Data model for validation results."""
    query: str
    results: List[RetrievalResult]
    execution_time: float
    consistency_score: float
    metadata_completeness: float


@dataclass
class ValidationMetrics:
    """Data model for validation metrics."""
    relevance_rate: float
    stability_rate: float
    metadata_accuracy: float
    response_time_variance: float


def embed_text(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    try:
        # Add a small delay to be respectful to the API
        time.sleep(0.1)

        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Using the same model as the ingestion pipeline
            input_type="search_query"  # Appropriate for search queries
        )
        logger.info(f"Successfully generated embeddings for {len(texts)} text(s)")
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


import time
from typing import Optional


def search_similar_content(query_text: str, top_k: int = 5, max_retries: int = 3, retry_delay: float = 1.0) -> List[RetrievalResult]:
    """
    Perform semantic similarity search against Qdrant collection.

    Args:
        query_text: Text to find similar content for
        top_k: Number of results to return (default: 5)
        max_retries: Maximum number of retry attempts for Qdrant connection issues (default: 3)
        retry_delay: Delay between retries in seconds (default: 1.0)

    Returns:
        List of RetrievalResult objects
    """
    # Validate query text
    if not query_text or not query_text.strip():
        logger.warning("Empty or whitespace-only query provided")
        return []

    # Check for very long queries (more than 500 characters)
    if len(query_text) > 500:
        logger.warning(f"Query too long: '{query_text[:50]}...'. Maximum length is 500 characters. Truncating to first 500 characters.")
        query_text = query_text[:500]

    # Check for very short queries (less than 2 characters)
    query_stripped = query_text.strip()
    if len(query_stripped) < 2:
        logger.warning(f"Query too short: '{query_text}'. Minimum length is 2 characters.")
        return []

    # Check for overly general queries (common single words)
    general_terms = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    if query_stripped.lower() in general_terms:
        logger.warning(f"Overly general query detected: '{query_text}'. This may not yield meaningful results.")
        return []

    # Generate embedding for the query text
    query_embeddings = embed_text([query_text])
    if not query_embeddings or len(query_embeddings) == 0:
        logger.error("Failed to generate embedding for query text")
        return []

    query_vector = query_embeddings[0]

    # Attempt search with retry logic for Qdrant availability
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Starting semantic search for query: '{query_text[:50]}...' (Attempt {attempt + 1})")

            # Perform search in Qdrant using query_points (newer API)
            search_results = qdrant_client.query_points(
                collection_name="rag_embedding",
                query=query_vector,
                limit=top_k,
                with_payload=True,  # Include metadata
            )

            # Format results - query_points returns a response object with points
            results = []
            for hit in search_results.points:
                result = RetrievalResult(
                    id=hit.id,
                    score=hit.score,
                    content=hit.payload.get('content', ''),
                    metadata=hit.payload
                )
                results.append(result)

            if len(results) == 0:
                logger.warning(f"No relevant documents found for query: '{query_text[:50]}...'")
            else:
                logger.info(f"Successfully found {len(results)} similar results for query: '{query_text[:50]}...'")

            return results

        except Exception as e:
            last_exception = e
            error_msg = str(e).lower()

            # Check if it's a connection-related error that warrants a retry
            if any(keyword in error_msg for keyword in ['connection', 'timeout', 'network', 'connect', 'refused', 'unavailable', '503', '504']):
                if attempt < max_retries:
                    logger.warning(f"Qdrant connection issue (attempt {attempt + 1}), retrying in {retry_delay}s: {str(e)}")
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error(f"Qdrant connection failed after {max_retries} retries: {str(e)}")
            else:
                # For non-connection errors, don't retry
                logger.error(f"Error searching for similar content: {str(e)}", exc_info=True)
                break

    # If all retries failed, log the final error
    if last_exception:
        logger.error(f"Failed to retrieve content after {max_retries + 1} attempts: {str(last_exception)}", exc_info=True)

    return []


def validate_retrieval_pipeline(queries: List[str], runs: int = 10) -> ValidationResult:
    """
    Validate the retrieval pipeline by running queries multiple times.

    Args:
        queries: List of query strings to test
        runs: Number of times to execute each query (default: 10)

    Returns:
        ValidationResult object with consistency and performance metrics
    """
    import time
    from collections import defaultdict

    logger.info(f"Starting retrieval pipeline validation with {len(queries)} queries, {runs} runs each")

    all_results = []
    execution_times = []

    for run in range(runs):
        logger.info(f"Starting run {run + 1}/{runs}")

        for query in queries:
            start_time = time.time()

            try:
                results = search_similar_content(query, top_k=5)
                end_time = time.time()

                execution_time = end_time - start_time
                execution_times.append(execution_time)

                all_results.append({
                    'query': query,
                    'run': run,
                    'results': results,
                    'execution_time': execution_time
                })

                logger.debug(f"Run {run + 1}: Query '{query[:30]}...' completed in {execution_time:.3f}s with {len(results)} results")

            except Exception as e:
                logger.error(f"Run {run + 1}: Error processing query '{query}': {str(e)}")
                # Continue with other queries even if one fails

    # Calculate metrics
    total_queries = len(queries) * runs
    successful_queries = len(all_results)

    if successful_queries > 0:
        avg_execution_time = sum(execution_times) / len(execution_times)
        execution_time_variance = sum((t - avg_execution_time) ** 2 for t in execution_times) / len(execution_times) if execution_times else 0
    else:
        avg_execution_time = 0
        execution_time_variance = 0

    # Calculate consistency score (simplified - compares result IDs across runs)
    consistency_score = calculate_consistency_score(all_results, queries, runs)

    # Calculate metadata completeness
    metadata_completeness = calculate_metadata_completeness(all_results)

    # Create and return ValidationResult
    validation_result = ValidationResult(
        query="; ".join(queries),  # Combine all queries for the validation result
        results=[],  # Placeholder - actual results would be in the validation process
        execution_time=avg_execution_time,
        consistency_score=consistency_score,
        metadata_completeness=metadata_completeness
    )

    logger.info(f"Pipeline validation completed. Success rate: {successful_queries}/{total_queries}, "
                f"Avg execution time: {avg_execution_time:.3f}s, Consistency score: {consistency_score:.3f}")

    return validation_result


def calculate_consistency_score(all_results: List[Dict], queries: List[str], runs: int) -> float:
    """
    Calculate consistency score based on how similar results are across multiple runs.

    Args:
        all_results: List of all results from all runs
        queries: Original queries that were run
        runs: Number of runs performed

    Returns:
        Consistency score between 0.0 and 1.0
    """
    if not all_results:
        return 0.0

    # Group results by query
    query_results = defaultdict(list)
    for result in all_results:
        query_results[result['query']].append(result)

    # For each query, check consistency across runs
    total_consistency = 0.0
    valid_queries = 0

    for query, runs_results in query_results.items():
        if len(runs_results) < 2:  # Need at least 2 runs to check consistency
            continue

        # Calculate consistency by comparing top result IDs across runs
        top_result_ids = []
        for run_result in runs_results:
            if run_result['results']:
                # Use the ID of the top result for consistency check
                top_result_ids.append(run_result['results'][0].id if run_result['results'] else None)

        # Calculate how many runs had the same top result
        if top_result_ids:
            most_common_id = max(set(top_result_ids), key=top_result_ids.count)
            consistency = top_result_ids.count(most_common_id) / len(top_result_ids)
            total_consistency += consistency
            valid_queries += 1

    # Return average consistency across all queries
    if valid_queries > 0:
        return total_consistency / valid_queries
    else:
        return 0.0


def calculate_metadata_completeness(all_results: List[Dict]) -> float:
    """
    Calculate metadata completeness based on how complete the metadata is in results.

    Args:
        all_results: List of all results from all runs

    Returns:
        Metadata completeness score between 0.0 and 1.0
    """
    if not all_results:
        return 0.0

    total_metadata_fields = 0
    expected_metadata_fields = 0

    for result in all_results:
        for retrieval_result in result['results']:
            # Expected fields: url, title, content, and other payload fields
            expected_fields = ['url', 'title', 'content']
            total_metadata_fields += len(retrieval_result.metadata)

            for field in expected_fields:
                if field in retrieval_result.metadata:
                    expected_metadata_fields += 1

    if expected_metadata_fields == 0:
        return 1.0 if total_metadata_fields == 0 else 0.0

    # Calculate percentage of expected metadata fields that are present
    return expected_metadata_fields / (expected_metadata_fields + len(all_results) * len(expected_fields) if all_results else 1)


def validate_metadata_retrieval(test_queries: Optional[List[str]] = None) -> ValidationMetrics:
    """
    Verify that metadata is correctly returned with retrieved chunks.

    Args:
        test_queries: Optional list of test queries (uses default if not provided)

    Returns:
        ValidationMetrics object focusing on metadata accuracy
    """
    if test_queries is None:
        test_queries = ["What is AI?", "Machine Learning", "Retrieval Augmented Generation", "Python programming"]

    logger.info(f"Starting metadata validation with {len(test_queries)} test queries")

    total_metadata_fields = 0
    expected_metadata_fields = 0
    total_results = 0

    for query in test_queries:
        try:
            results = search_similar_content(query, top_k=3)
            for result in results:
                total_results += 1
                # Expected fields that should be present in metadata
                expected_fields = ['url', 'title', 'content']

                for field in expected_fields:
                    if field in result.metadata:
                        expected_metadata_fields += 1

                # Count total fields in metadata
                total_metadata_fields += len(result.metadata)

        except Exception as e:
            logger.error(f"Error validating metadata for query '{query}': {str(e)}")
            continue

    # Calculate metadata accuracy
    metadata_accuracy = 0.0
    if total_results > 0 and expected_metadata_fields > 0:
        # Calculate the percentage of expected metadata fields that are present
        metadata_accuracy = expected_metadata_fields / (total_results * 3)  # 3 expected fields per result

    # For this function, we'll return a ValidationMetrics object with metadata accuracy
    # Other metrics are set to default values since this function focuses on metadata
    validation_metrics = ValidationMetrics(
        relevance_rate=0.0,  # Not calculated in this function
        stability_rate=0.0,  # Not calculated in this function
        metadata_accuracy=metadata_accuracy,
        response_time_variance=0.0  # Not calculated in this function
    )

    logger.info(f"Metadata validation completed. Accuracy: {metadata_accuracy:.3f} across {total_results} results")

    return validation_metrics


def calculate_relevance_score(query: str, result_content: str) -> float:
    """
    Calculate relevance of a result to the original query.

    Args:
        query: Original query text
        result_content: Content of retrieved result

    Returns:
        Float representing relevance score (0.0-1.0)
    """
    if not query or not result_content:
        return 0.0

    # Convert both to lowercase for comparison
    query_lower = query.lower()
    content_lower = result_content.lower()

    # Split into words
    query_words = set(query_lower.split())
    content_words = set(content_lower.split())

    # Calculate Jaccard similarity (intersection over union)
    intersection = query_words.intersection(content_words)
    union = query_words.union(content_words)

    jaccard_similarity = len(intersection) / len(union) if union else 0.0

    # Calculate word overlap ratio
    overlap_ratio = len(intersection) / len(query_words) if query_words else 0.0

    # Combine both measures with weights
    # Jaccard similarity gives overall similarity
    # Overlap ratio gives how much of the query is covered
    relevance_score = 0.5 * jaccard_similarity + 0.5 * overlap_ratio

    # Ensure the score is between 0 and 1
    return min(1.0, max(0.0, relevance_score))


def calculate_validation_metrics(all_results: List[Dict], queries: List[str], runs: int) -> ValidationMetrics:
    """
    Calculate comprehensive validation metrics for the retrieval pipeline.

    Args:
        all_results: List of all results from all runs
        queries: Original queries that were run
        runs: Number of runs performed

    Returns:
        ValidationMetrics object with all calculated metrics
    """
    if not all_results:
        return ValidationMetrics(
            relevance_rate=0.0,
            stability_rate=0.0,
            metadata_accuracy=0.0,
            response_time_variance=0.0
        )

    # Calculate execution times for variance
    execution_times = [result['execution_time'] for result in all_results if 'execution_time' in result]
    avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
    response_time_variance = sum((t - avg_execution_time) ** 2 for t in execution_times) / len(execution_times) if len(execution_times) > 1 else 0

    # Calculate consistency score
    consistency_score = calculate_consistency_score(all_results, queries, runs)

    # Calculate metadata completeness
    metadata_completeness = calculate_metadata_completeness(all_results)

    # For relevance rate, we'll use a simplified approach based on scores
    relevance_count = 0
    total_results = 0

    for result in all_results:
        for retrieval_result in result.get('results', []):
            total_results += 1
            # Consider a result relevant if its score is above a threshold (e.g., 0.5)
            if retrieval_result.score > 0.5:
                relevance_count += 1

    relevance_rate = relevance_count / total_results if total_results > 0 else 0.0

    return ValidationMetrics(
        relevance_rate=relevance_rate,
        stability_rate=consistency_score,
        metadata_accuracy=metadata_completeness,
        response_time_variance=response_time_variance
    )


import sys
import argparse

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Retrieve similar content from Qdrant')
    parser.add_argument('--query', type=str, help='Query text to search for similar content')
    parser.add_argument('--top_k', type=int, default=5, help='Number of results to return (default: 5)')

    args = parser.parse_args()

    if args.query:
        query_text = args.query
    else:
        query_text = "What is AI?"  # Default query

    print("Retrieval module loaded successfully")
    print(f"Searching for: '{query_text}'")
    print("Testing basic search functionality...")

    # Test with the provided query
    sample_results = search_similar_content(query_text, top_k=args.top_k)
    print(f"Found {len(sample_results)} results")

    for i, result in enumerate(sample_results):
        print(f"Result {i+1}: Score: {result.score:.4f}, Content snippet: {result.content[:100]}...")
        print(f"  Metadata: {result.metadata.get('title', 'No title')}")
        print(f"  URL: {result.metadata.get('url', 'No URL')}")
        print("---")