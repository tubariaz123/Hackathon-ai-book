# Implementation Plan: Retrieval and pipeline validation

**Feature**: Retrieval and pipeline validation
**Branch**: 006-retrieval-validation
**Created**: 2025-12-25
**Status**: Draft
**Input**: Create a single file `retrieve.py` in the backend folder - Connect to Qdrant collection - Run semantic similarity queries - Retrieve top-k chunks with metadata - Verify relevance and stability

## Technical Context

- **Target Architecture**: Python backend with Qdrant vector database
- **File to create**: `backend/retrieve.py`
- **Primary Function**: Semantic similarity queries against Qdrant collection
- **Key Components**: Connection to Qdrant, query execution, result validation
- **Qdrant Connection**: Using QDRANT_URL and QDRANT_API_KEY from environment variables, connecting via HTTPS
- **Collection Name**: "rag_embedding" (as used in existing ingestion pipeline)
- **Embedding Model**: Cohere's "embed-english-v3.0" with 1024-dimensional vectors using cosine distance
- **Top-K Value**: 5 results (standard for retrieval validation, matches spec requirements)
- **Validation Method**: Relevance via semantic similarity scores and content matching, stability via repeated query execution

## Constitution Check

- ✅ Spec-First Authoring: Proceeding with implementation based on approved spec
- ✅ Technical Accuracy and Reproducibility: Code is testable and reproducible with validation framework
- ✅ Strict RAG Grounding: Retrieval functionality aligns with grounding requirements
- ✅ Separation of Content, AI, and Infrastructure: Focusing on retrieval layer
- ✅ Deterministic Content Processing: Implemented stable and repeatable retrieval with validation
- ✅ Quality-Driven Publication Pipeline: Includes comprehensive validation functionality

## Phase 0: Research

### Research Summary

All research tasks completed and documented in [research.md](research.md):

1. **Qdrant Connection Details**: Connection uses QDRANT_URL and QDRANT_API_KEY from environment variables with HTTPS
2. **Qdrant Query API**: Semantic similarity search uses `qdrant_client.search()` method with query_vector, limit, and with_payload parameters
3. **Embedding Compatibility**: Cohere's "embed-english-v3.0" model with 1024-dimensional vectors using "search_document" input type
4. **Validation Approaches**: Relevance via similarity scores and content matching, stability via repeated execution validation

## Phase 1: Design

### Data Model

Based on the existing system and feature requirements, the following data models are relevant:

#### Query Model
- **query_text**: (string) The input text to search for similar content
- **top_k**: (integer) Number of results to retrieve (default: 5)
- **filters**: (dict, optional) Metadata filters to apply to the search

#### RetrievalResult Model
- **id**: (string) Unique identifier for the retrieved chunk
- **score**: (float) Semantic similarity score (0.0-1.0)
- **content**: (string) The text content of the retrieved chunk
- **metadata**: (dict) Associated metadata including url, title, chunk_index
- **relevance**: (float) Calculated relevance score based on query

#### ValidationResult Model
- **query**: (string) The original query text
- **results**: (list) List of RetrievalResult objects
- **execution_time**: (float) Time taken to execute the query in seconds
- **consistency_score**: (float) Measure of result stability across multiple runs
- **metadata_completeness**: (float) Percentage of expected metadata fields present

#### ValidationMetrics Model
- **relevance_rate**: (float) Percentage of relevant results in top-k
- **stability_rate**: (float) Percentage of consistent results across runs
- **metadata_accuracy**: (float) Percentage of complete metadata retrieval
- **response_time_variance**: (float) Variance in response times across runs

### API Contracts

Based on the functional requirements, the following API contracts will be implemented in the retrieve.py module:

#### Function: search_similar_content(query_text, top_k=5)
- **Purpose**: Perform semantic similarity search against Qdrant collection
- **Input**:
  - query_text (string): Text to find similar content for
  - top_k (integer, optional): Number of results to return (default: 5)
- **Output**: List of RetrievalResult objects
- **Error handling**: Raises exceptions for connection issues, invalid queries
- **Dependencies**: QdrantClient, Cohere client for embedding generation

#### Function: validate_retrieval_pipeline(queries, runs=10)
- **Purpose**: Validate the retrieval pipeline by running queries multiple times
- **Input**:
  - queries (list): List of query strings to test
  - runs (integer, optional): Number of times to execute each query (default: 10)
- **Output**: ValidationResult object with consistency and performance metrics
- **Error handling**: Reports failures and provides partial results if possible

#### Function: validate_metadata_retrieval()
- **Purpose**: Verify that metadata is correctly returned with retrieved chunks
- **Input**: None (uses test queries)
- **Output**: ValidationMetrics object focusing on metadata accuracy
- **Error handling**: Reports missing or incorrect metadata fields

#### Function: calculate_relevance_score(query, result_content)
- **Purpose**: Calculate relevance of a result to the original query
- **Input**:
  - query (string): Original query text
  - result_content (string): Content of retrieved result
- **Output**: Float representing relevance score (0.0-1.0)
- **Dependencies**: Text similarity algorithms or additional NLP models

### Quickstart Guide

#### Setup
1. Ensure environment variables are set:
   - `QDRANT_URL`: Your Qdrant cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key
   - `COHERE_API_KEY`: Your Cohere API key

2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

#### Basic Usage
1. Import the retrieval module:
   ```python
   from backend.retrieve import search_similar_content
   ```

2. Perform a semantic search:
   ```python
   results = search_similar_content("Your query text here", top_k=5)
   for result in results:
       print(f"Score: {result.score}, Content: {result.content[:100]}...")
   ```

#### Validation Usage
1. Validate the entire retrieval pipeline:
   ```python
   from backend.retrieve import validate_retrieval_pipeline

   test_queries = ["Sample query 1", "Sample query 2", "Sample query 3"]
   validation_results = validate_retrieval_pipeline(test_queries, runs=10)
   print(f"Relevance rate: {validation_results.relevance_rate}")
   print(f"Stability rate: {validation_results.consistency_score}")
   ```

#### Environment Setup
- Copy `.env.example` to `.env` and fill in your API keys
- Ensure the Qdrant collection "rag_embedding" exists with data
- Verify Cohere API access for embedding generation

## Phase 2: Implementation

### Tasks

1. **Create retrieve.py module**: Set up the basic file structure with necessary imports
2. **Implement Qdrant connection**: Create connection function using environment variables
3. **Implement embedding generation**: Function to convert query text to embeddings using Cohere
4. **Implement search function**: Create search_similar_content function with semantic similarity
5. **Implement result validation**: Create functions to validate relevance and metadata
6. **Implement stability validation**: Create functions to test result consistency across runs
7. **Add error handling**: Proper exception handling for network and API issues
8. **Add logging**: Implement logging for debugging and monitoring
9. **Write unit tests**: Create tests for each function to ensure reliability

## Phase 3: Validation

### Testing Strategy

#### Unit Tests
- Test embedding generation with various input texts
- Test search function with known queries against test data
- Test metadata validation functions
- Test error handling for connection failures
- Test validation metric calculations

#### Integration Tests
- Test end-to-end retrieval pipeline with real Qdrant connection
- Validate that retrieved results match expected content
- Test metadata completeness and accuracy
- Verify stability across multiple query executions

#### Performance Tests
- Measure query response times under various loads
- Test consistency of results across different time periods
- Validate that top-k parameter works correctly
- Verify memory usage during retrieval operations

### Risk Assessment

- **Qdrant Connection**: Risk of network failures or API rate limits; implement retry logic and proper error handling
- **Embedding Consistency**: Risk of using wrong embedding model; ensure same model used for queries as for stored data
- **Performance**: Risk of slow query responses; implement caching and optimize search parameters
- **Data Drift**: Risk of schema changes in metadata; implement flexible payload handling

### Dependencies

- **Primary**: Qdrant cloud instance with existing "rag_embedding" collection
- **API Keys**: Valid QDRANT_API_KEY and COHERE_API_KEY in environment
- **Embedding Model**: Cohere's embed-english-v3.0 model access
- **Python Packages**: qdrant-client, cohere, python-dotenv (already in requirements.txt)

### Success Criteria

- ✅ Semantic similarity search returns relevant results for test queries
- ✅ Metadata is correctly retrieved with each result
- ✅ Retrieval pipeline shows consistent results across 10 consecutive runs
- ✅ Response times are stable with less than 5% variance
- ✅ All expected metadata fields are returned with retrieved chunks
- ✅ Module passes all unit and integration tests
