"""
Qdrant Semantic Similarity Search Guide

This file demonstrates how to perform semantic similarity searches with Qdrant
based on the existing code in backend/src/main.py. The implementation shows
various search methods available in the Qdrant Python client.

Key aspects of semantic similarity search with Qdrant:
1. QdrantClient is used with url and api_key
2. Cohere's embed-english-v3.0 model is used (1024-dimensional vectors)
3. Collections are created with cosine distance
4. Data is stored with metadata
5. Search operations find similar vectors and return results with metadata
"""

import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def basic_search_example(query_vector, collection_name="rag_embedding", limit=5):
    """
    Basic semantic similarity search using query_points method.

    Args:
        query_vector (list): Vector to search for similar items
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return

    Returns:
        list: Search results with scores and metadata
    """
    try:
        # Perform search using query_points
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,  # Include metadata
            with_vectors=False  # We don't need the vectors back
        )

        # Process results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
            }
            results.append(result)

        logger.info(f"Found {len(results)} results for search")
        return results

    except Exception as e:
        logger.error(f"Error performing search: {str(e)}")
        return []


def search_with_filters_example(query_vector, collection_name="rag_embedding", limit=5, filters=None):
    """
    Search with optional filters using query_points method.

    Args:
        query_vector (list): Vector to search for similar items
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return
        filters (dict): Optional filter conditions

    Returns:
        list: Filtered search results with scores and metadata
    """
    try:
        # Build filter if provided
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                # Create a 'must' condition for each filter
                condition = models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
                conditions.append(condition)

            if conditions:
                qdrant_filter = models.Filter(must=conditions)

        # Perform search with filters
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=qdrant_filter,  # Apply filters
            limit=limit,
            with_payload=True,  # Include metadata
            with_vectors=False  # We don't need the vectors back
        )

        # Process results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
            }
            results.append(result)

        logger.info(f"Found {len(results)} filtered results")
        return results

    except Exception as e:
        logger.error(f"Error performing filtered search: {str(e)}")
        return []


def search_with_score_threshold(query_vector, collection_name="rag_embedding", limit=5, score_threshold=0.5):
    """
    Search with a minimum score threshold to filter out low-quality matches.

    Args:
        query_vector (list): Vector to search for similar items
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return
        score_threshold (float): Minimum similarity score threshold

    Returns:
        list: Search results with scores above threshold
    """
    try:
        # Perform search with score threshold
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,  # Set minimum score threshold
            with_payload=True,
            with_vectors=False
        )

        # Process results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
            }
            results.append(result)

        logger.info(f"Found {len(results)} results with score >= {score_threshold}")
        return results

    except Exception as e:
        logger.error(f"Error performing search with score threshold: {str(e)}")
        return []


def batch_search_example(queries, collection_name="rag_embedding", limit=5):
    """
    Perform multiple searches in a batch to optimize network requests.

    Args:
        queries (list): List of query vectors
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return per query

    Returns:
        list: List of search results for each query
    """
    try:
        # Create batch search requests
        search_requests = []
        for query_vector in queries:
            search_request = models.QueryRequest(
                query=query_vector,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            search_requests.append(search_request)

        # Perform batch search
        batch_results = qdrant_client.query_batch_points(
            collection_name=collection_name,
            requests=search_requests
        )

        # Process results
        all_results = []
        for query_idx, query_results in enumerate(batch_results):
            query_results_formatted = []
            for hit in query_results.points:
                result = {
                    'id': hit.id,
                    'score': hit.score,
                    'payload': hit.payload,
                    'url': hit.payload.get('url', 'N/A'),
                    'title': hit.payload.get('title', 'N/A'),
                }
                query_results_formatted.append(result)
            all_results.append(query_results_formatted)

        logger.info(f"Completed batch search for {len(queries)} queries")
        return all_results

    except Exception as e:
        logger.error(f"Error performing batch search: {str(e)}")
        return []


def advanced_search_example(query_vector, collection_name="rag_embedding", limit=5):
    """
    Advanced search with custom parameters and search configuration.

    Args:
        query_vector (list): Vector to search for similar items
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return

    Returns:
        list: Advanced search results with detailed information
    """
    try:
        # Advanced search with custom parameters
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            # Additional search parameters
            params=models.SearchParams(
                hnsw_ef=128,  # Size of the beam in a beam-search
                exact=False,   # Use approximate search for performance
                indexed_only=False  # Search all vectors, not just indexed ones
            ),
            with_payload=True,
            with_vectors=False
        )

        # Process results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
                'chunk_index': hit.payload.get('chunk_index', 'N/A'),
                'original_content_length': hit.payload.get('original_content_length', 'N/A'),
            }
            results.append(result)

        logger.info(f"Found {len(results)} advanced search results")
        return results

    except Exception as e:
        logger.error(f"Error performing advanced search: {str(e)}")
        return []


def search_by_payload_example(collection_name="rag_embedding", limit=5, payload_filter=None):
    """
    Search for points based on payload (metadata) conditions without semantic similarity.

    Args:
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return
        payload_filter (dict): Filter conditions for payload fields

    Returns:
        list: Points matching the payload filter
    """
    try:
        # Build filter for payload search
        if payload_filter:
            conditions = []
            for key, value in payload_filter.items():
                condition = models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
                conditions.append(condition)

            qdrant_filter = models.Filter(must=conditions)
        else:
            qdrant_filter = None

        # Use scroll method to retrieve points based on payload
        points, next_offset = qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=qdrant_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )

        # Process results
        results = []
        for point in points:
            result = {
                'id': point.id,
                'payload': point.payload,
                'url': point.payload.get('url', 'N/A'),
                'title': point.payload.get('title', 'N/A'),
            }
            results.append(result)

        logger.info(f"Found {len(results)} points matching payload filter")
        return results

    except Exception as e:
        logger.error(f"Error performing payload-based search: {str(e)}")
        return []


def retrieve_specific_points_example(point_ids, collection_name="rag_embedding"):
    """
    Retrieve specific points by their IDs to get their full information.

    Args:
        point_ids (list): List of point IDs to retrieve
        collection_name (str): Name of the collection to search in

    Returns:
        list: Retrieved points with their information
    """
    try:
        # Retrieve specific points by ID
        points = qdrant_client.retrieve(
            collection_name=collection_name,
            ids=point_ids,
            with_payload=True,
            with_vectors=False
        )

        # Process results
        results = []
        for point in points:
            result = {
                'id': point.id,
                'payload': point.payload,
                'url': point.payload.get('url', 'N/A'),
                'title': point.payload.get('title', 'N/A'),
            }
            results.append(result)

        logger.info(f"Retrieved {len(results)} specific points")
        return results

    except Exception as e:
        logger.error(f"Error retrieving specific points: {str(e)}")
        return []


def count_points_example(collection_name="rag_embedding", filters=None):
    """
    Count points in the collection that match certain conditions.

    Args:
        collection_name (str): Name of the collection to count in
        filters (dict): Optional filter conditions

    Returns:
        int: Number of points matching the conditions
    """
    try:
        # Build filter if provided
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                condition = models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
                conditions.append(condition)

            qdrant_filter = models.Filter(must=conditions)

        # Count points
        count_result = qdrant_client.count(
            collection_name=collection_name,
            count_filter=qdrant_filter
        )

        logger.info(f"Found {count_result.count} points matching criteria")
        return count_result.count

    except Exception as e:
        logger.error(f"Error counting points: {str(e)}")
        return 0


# Example usage
if __name__ == "__main__":
    # Example of how to use the search functions
    print("Qdrant Semantic Similarity Search Guide")
    print("=" * 50)

    # Example query vector (in real usage, this would come from your embedding model)
    example_query_vector = [0.1] * 1024  # Example 1024-dimensional vector

    # Basic search
    print("\n1. Basic Search:")
    basic_results = basic_search_example(example_query_vector)
    for i, result in enumerate(basic_results[:2]):  # Show first 2 results
        print(f"  Result {i+1}: ID={result['id']}, Score={result['score']:.4f}, Title={result['title']}")

    # Search with filters
    print("\n2. Search with Filters:")
    filters = {"title": "AI"}  # Example filter
    filtered_results = search_with_filters_example(example_query_vector, filters=filters)
    for i, result in enumerate(filtered_results[:2]):  # Show first 2 results
        print(f"  Result {i+1}: ID={result['id']}, Score={result['score']:.4f}, Title={result['title']}")

    # Search with score threshold
    print("\n3. Search with Score Threshold:")
    threshold_results = search_with_score_threshold(example_query_vector, score_threshold=0.1)
    for i, result in enumerate(threshold_results[:2]):  # Show first 2 results
        print(f"  Result {i+1}: ID={result['id']}, Score={result['score']:.4f}, Title={result['title']}")

    # Count points
    print("\n4. Count Points:")
    count = count_points_example()
    print(f"  Total points in collection: {count}")

    print("\nSearch guide completed!")