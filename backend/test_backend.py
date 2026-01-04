#!/usr/bin/env python3
"""
Test script to check if the backend can connect to Qdrant and retrieve documents.
"""
import os
import sys
import logging

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from retrieve import search_similar_content, RetrievalResult
from agent import create_rag_agent, query_agent

def test_qdrant_connection():
    """Test if we can connect to Qdrant and retrieve documents."""
    print("Testing Qdrant connection and document retrieval...")

    # Test query to see if we can retrieve any documents
    test_query = "Introduction to ROS 2"
    print(f"Searching for: '{test_query}'")

    try:
        results = search_similar_content(test_query, top_k=5)
        print(f"Found {len(results)} results")

        if results:
            print("Sample results:")
            for i, result in enumerate(results[:3]):  # Show first 3 results
                print(f"  Result {i+1}: Score: {result.score:.4f}")
                print(f"    Content: {result.content[:200]}...")
                print(f"    Metadata: {result.metadata}")
                print()
        else:
            print("No documents found. This may indicate:")
            print("  1. Qdrant collection is empty")
            print("  2. Qdrant connection issues")
            print("  3. API keys are incorrect")
            print("  4. The collection 'rag_embedding' doesn't exist")

        return len(results) > 0

    except Exception as e:
        print(f"Error during search: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_query():
    """Test if the agent can process queries."""
    print("\nTesting agent query processing...")

    try:
        # Create an agent
        agent = create_rag_agent(model_name="gpt-4-turbo")
        print("Agent created successfully")

        # Test a simple query
        test_query = "Introduction to ROS 2 for Physical AI"
        print(f"Processing query: '{test_query}'")

        response = query_agent(agent, test_query, top_k=5)
        print(f"Response: {response.answer}")
        print(f"Confidence: {response.confidence}")
        print(f"Sources: {len(response.sources)}")

        return True

    except Exception as e:
        print(f"Error during agent query: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running backend connectivity tests...\n")

    # Test Qdrant connection
    qdrant_ok = test_qdrant_connection()

    # Test agent query if Qdrant is working
    if qdrant_ok:
        agent_ok = test_agent_query()
    else:
        print("\nSkipping agent test due to Qdrant connection issues")
        agent_ok = False

    print(f"\nTest Results:")
    print(f"  Qdrant Connection: {'PASS' if qdrant_ok else 'FAIL'}")
    print(f"  Agent Query: {'PASS' if agent_ok else 'FAIL'}")

    if not qdrant_ok:
        print("\nThe issue is likely that the Qdrant collection doesn't contain the required documents.")
        print("You need to ensure the documents about ROS 2 and Physical AI are ingested into Qdrant.")