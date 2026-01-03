# Backend: Retrieval and Pipeline Validation

This directory contains the backend implementation for the retrieval and pipeline validation system. The system provides semantic similarity search capabilities against a Qdrant vector database and tools to validate the retrieval pipeline.

## Features

- **Semantic Search**: Perform semantic similarity searches using Cohere embeddings
- **Pipeline Validation**: Validate retrieval pipeline stability and consistency
- **Metadata Retrieval**: Retrieve document chunks with complete metadata
- **Relevance Scoring**: Calculate relevance of results to queries
- **Edge Case Handling**: Robust handling of various query types and error conditions

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit the .env file with your actual keys
   QDRANT_URL="your_qdrant_url"
   QDRANT_API_KEY="your_qdrant_api_key"
   COHERE_API_KEY="your_cohere_api_key"
   ```

## Usage

### Basic Semantic Search

```python
from retrieve import search_similar_content

# Search for similar content
results = search_similar_content("What is artificial intelligence?", top_k=5)

for result in results:
    print(f"Score: {result.score}")
    print(f"Content: {result.content[:200]}...")
    print(f"Metadata: {result.metadata}")
    print("---")
```

### Pipeline Validation

```python
from retrieve import validate_retrieval_pipeline

# Validate the retrieval pipeline with multiple queries
queries = ["What is AI?", "Machine Learning", "Python programming"]
validation_result = validate_retrieval_pipeline(queries, runs=10)

print(f"Consistency score: {validation_result.consistency_score}")
print(f"Execution time: {validation_result.execution_time}")
print(f"Metadata completeness: {validation_result.metadata_completeness}")
```

### Metadata Validation

```python
from retrieve import validate_metadata_retrieval

# Validate that metadata is correctly retrieved
metrics = validate_metadata_retrieval()
print(f"Metadata accuracy: {metrics.metadata_accuracy}")
```

### Relevance Scoring

```python
from retrieve import calculate_relevance_score

# Calculate how relevant content is to a query
relevance = calculate_relevance_score("artificial intelligence", "AI is a branch of computer science...")
print(f"Relevance score: {relevance}")
```

## Configuration

The `search_similar_content` function accepts the following parameters:

- `query_text`: The text to search for similar content
- `top_k`: Number of results to return (default: 5)
- `max_retries`: Maximum number of retry attempts for Qdrant connection issues (default: 3)
- `retry_delay`: Delay between retries in seconds (default: 1.0)

## Error Handling

The system handles various edge cases:

- Empty or whitespace-only queries
- Very short queries (less than 2 characters)
- Overly general queries (common single words)
- Very long queries (truncated to 500 characters)
- Qdrant connection issues (with retry logic)
- Cohere API errors
- Missing metadata fields

## Architecture

The system consists of the following key components:

- **Qdrant Client**: Vector database for storing and searching embeddings
- **Cohere Client**: Text embedding generation
- **Data Models**: Structured data classes for queries, results, and validation
- **Validation Functions**: Tools for pipeline validation and metrics calculation

## Environment Variables

- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant access
- `COHERE_API_KEY`: API key for Cohere embedding service

## RAG AI Agent

The RAG (Retrieval-Augmented Generation) AI Agent provides a way to query book content using AI while ensuring responses are grounded in retrieved context.

### Setup

1. **Additional Environment Variables**: Add these to your `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Install Dependencies**: Make sure to install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure Qdrant Collection**: Verify that the Qdrant collection "rag_embedding" exists with data.

### Usage

#### Running the API Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### API Endpoints

- `GET /health`: Health check endpoint
- `POST /query`: Process a query through the RAG agent
- `GET /models`: List available models
- `POST /query_simple`: Simple query endpoint

#### Example Query
```python
from backend.agent import create_rag_agent, query_agent

# Initialize the RAG agent
agent = create_rag_agent(model_name="gpt-4-turbo")

# Query the agent
response = query_agent(agent, "Your question here", top_k=5)
print(f"Answer: {response.answer}")
print(f"Sources: {response.sources}")
```

### Features

- **Grounded Responses**: Ensures all responses are based only on retrieved content
- **Source Attribution**: Provides source information for all answers
- **Confidence Scoring**: Returns confidence scores based on retrieval quality
- **Error Handling**: Comprehensive error handling for API and retrieval failures
- **Flexible Configuration**: Support for different OpenAI models and retrieval parameters