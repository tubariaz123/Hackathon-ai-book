# Qdrant Semantic Similarity Search Implementation Guide

Based on the existing code in `backend/src/main.py`, this document provides a comprehensive guide on how to perform semantic similarity searches with Qdrant. The implementation uses:

- **QdrantClient** with URL and API key for authentication
- **Cohere's embed-english-v3.0 model** (1024-dimensional vectors)
- **Cosine distance** for similarity calculation
- **Metadata storage** with each vector for rich search results

## Key Components

### 1. Client Initialization
```python
from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=60.0,  # Set timeout to 60 seconds
)
```

### 2. Collection Structure
```python
qdrant_client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=1024,  # Cohere embeddings are 1024-dimensional
        distance=models.Distance.COSINE  # Use cosine distance
    )
)
```

### 3. Vector Storage with Metadata
```python
qdrant_client.upsert(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=chunk_id,
            vector=embedding,  # 1024-dimensional vector
            payload=metadata   # Dictionary with additional information
        )
    ]
)
```

## Search Methods Available

### 1. Basic Semantic Search
The primary method for finding semantically similar content:

```python
def search_similar_content(query_text, collection_name="rag_embedding", limit=5):
    # Generate embedding for query text
    query_embeddings = embed([query_text])
    query_vector = query_embeddings[0]

    # Perform search in Qdrant
    search_results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True,   # Include metadata
        with_vectors=False   # Don't return vectors
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

    return results
```

### 2. Search with Filters
Filter results based on metadata conditions:

```python
def search_with_filters(query_text, collection_name="rag_embedding", limit=5, filters=None):
    # Generate embedding
    query_embeddings = embed([query_text])
    query_vector = query_embeddings[0]

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

        if conditions:
            qdrant_filter = models.Filter(must=conditions)

    # Perform search with filters
    search_results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=qdrant_filter,  # Apply filters
        limit=limit,
        with_payload=True,
        with_vectors=False
    )

    # Process results...
```

### 3. Advanced Search with Parameters
Customize search behavior with additional parameters:

```python
# Search with score threshold
search_results = qdrant_client.query_points(
    collection_name=collection_name,
    query=query_vector,
    limit=limit,
    score_threshold=0.5,    # Only return results with score >= 0.5
    params=models.SearchParams(
        hnsw_ef=128,        # Higher values = more accurate but slower
        exact=False,        # Use approximate search for performance
        indexed_only=False  # Search all vectors, not just indexed ones
    ),
    with_payload=True,
    with_vectors=False
)
```

## Available Filter Types

### 1. Exact Value Match
```python
filter = models.Filter(
    must=[
        models.FieldCondition(
            key="title",
            match=models.MatchValue(value="Introduction to AI")
        )
    ]
)
```

### 2. Text Search
```python
filter = models.Filter(
    must=[
        models.FieldCondition(
            key="content",
            match=models.MatchText(text="machine learning")
        )
    ]
)
```

### 3. Range Filters
```python
filter = models.Filter(
    must=[
        models.FieldCondition(
            key="word_count",
            range=models.Range(gte=100, lte=1000)
        )
    ]
)
```

### 4. Combined Filters (AND logic)
```python
filter = models.Filter(
    must=[
        models.FieldCondition(key="category", match=models.MatchValue(value="tech")),
        models.FieldCondition(key="published", range=models.Range(gte="2023-01-01"))
    ]
)
```

### 5. OR Logic
```python
filter = models.Filter(
    should=[
        models.FieldCondition(key="tag", match=models.MatchValue(value="AI")),
        models.FieldCondition(key="tag", match=models.MatchValue(value="ML"))
    ]
)
```

## Batch Search Operations

For multiple queries, use batch operations for efficiency:

```python
def batch_search_example(queries, collection_name="rag_embedding", limit=5):
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

    return batch_results
```

## Result Processing

Search results include:
- **ID**: Unique identifier for the stored vector
- **Score**: Similarity score (higher is more similar for cosine similarity)
- **Payload**: Metadata stored with the vector
- **URL/Title**: Content information from the stored metadata

## Performance Considerations

1. **Score Threshold**: Use `score_threshold` to filter low-quality results
2. **Limit Results**: Use `limit` to control the number of returned results
3. **Filter Early**: Apply filters to reduce search space
4. **Batch Operations**: Use batch methods when performing multiple searches
5. **HNSW Parameters**: Adjust `hnsw_ef` for performance vs accuracy trade-off

## Error Handling

Always wrap search operations in try-catch blocks:

```python
try:
    results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True
    )
    # Process results
except Exception as e:
    logger.error(f"Search failed: {str(e)}")
    # Handle error appropriately
```

## Complete Search Example

```python
def comprehensive_search(query_text, collection_name="rag_embedding", limit=5):
    try:
        # Generate embedding for query
        query_embeddings = embed([query_text])
        if not query_embeddings:
            return []

        query_vector = query_embeddings[0]

        # Perform search with multiple options
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            score_threshold=0.1,  # Minimum similarity
            params=models.SearchParams(
                hnsw_ef=128,
                exact=False
            ),
            with_payload=True,
            with_vectors=False
        )

        # Format results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
                'content_snippet': hit.payload.get('content', '')[:200] + '...'
            }
            results.append(result)

        return results

    except Exception as e:
        logger.error(f"Comprehensive search failed: {str(e)}")
        return []
```

This implementation provides a robust foundation for semantic similarity search in your application, allowing you to find relevant content based on meaning rather than exact keyword matches.