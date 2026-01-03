"""
Test script to demonstrate Qdrant semantic similarity search functionality.
This script shows how to use the search methods added to the main application.
"""

import os
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    timeout=60.0,
)

def embed(texts):
    """
    Generate embeddings for a list of texts using Cohere.
    """
    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return []

def test_search_functionality():
    """
    Test the search functionality with sample queries.
    """
    print("Testing Qdrant Semantic Similarity Search")
    print("=" * 50)

    # Sample search queries
    test_queries = [
        "What is artificial intelligence?",
        "How to build a neural network?",
        "Machine learning algorithms",
        "Python programming tutorial"
    ]

    collection_name = "rag_embedding"

    for i, query in enumerate(test_queries):
        print(f"\nTest {i+1}: Query = '{query}'")

        # Generate embedding for the query
        query_embeddings = embed([query])
        if not query_embeddings:
            print(f"  Failed to generate embedding for query: {query}")
            continue

        query_vector = query_embeddings[0]

        # Perform search
        try:
            search_results = qdrant_client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=3,  # Get top 3 results
                with_payload=True,
                with_vectors=False
            )

            print(f"  Found {len(search_results.points)} results:")
            for j, hit in enumerate(search_results.points):
                print(f"    {j+1}. Score: {hit.score:.4f}")
                print(f"       Title: {hit.payload.get('title', 'N/A')}")
                print(f"       URL: {hit.payload.get('url', 'N/A')}")
                print(f"       Chunk: {hit.payload.get('chunk_index', 'N/A')}")
                print()

        except Exception as e:
            print(f"  Error during search: {str(e)}")

def test_search_with_filters():
    """
    Test search functionality with filters.
    """
    print("\nTesting Search with Filters")
    print("=" * 30)

    query_text = "AI ethics"
    query_embeddings = embed([query_text])
    if not query_embeddings:
        print("Failed to generate embedding")
        return

    query_vector = query_embeddings[0]

    # Create a filter
    filter_condition = models.Filter(
        must=[
            models.FieldCondition(
                key="title",
                match=models.MatchText(text="AI")
            )
        ]
    )

    try:
        search_results = qdrant_client.query_points(
            collection_name="rag_embedding",
            query=query_vector,
            query_filter=filter_condition,
            limit=3,
            with_payload=True
        )

        print(f"Filtered search results for '{query_text}':")
        for i, hit in enumerate(search_results.points):
            print(f"  {i+1}. Score: {hit.score:.4f}, Title: {hit.payload.get('title', 'N/A')}")

    except Exception as e:
        print(f"Error during filtered search: {str(e)}")

def test_collection_info():
    """
    Test getting information about the collection.
    """
    print("\nTesting Collection Information")
    print("=" * 35)

    try:
        collection_info = qdrant_client.get_collection("rag_embedding")
        print(f"Collection name: {collection_info.config.params.vectors['size']} dimensions")
        print(f"Distance: {collection_info.config.params.vectors['distance']}")
        print(f"Points count: {collection_info.points_count}")

    except Exception as e:
        print(f"Error getting collection info: {str(e)}")

if __name__ == "__main__":
    print("Starting Qdrant Search Functionality Tests\n")

    # Test basic search
    test_search_functionality()

    # Test filtered search
    test_search_with_filters()

    # Test collection info
    test_collection_info()

    print("\nAll tests completed!")