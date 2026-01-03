"""
Qdrant Semantic Similarity Search - Complete Reference

Based on research of the Qdrant Python client implementation, this document provides
a comprehensive reference for performing semantic similarity searches with Qdrant.

Key Concepts:
1. Vector Similarity: Qdrant stores high-dimensional vectors and finds similar ones using distance metrics
2. Cosine Distance: Commonly used metric for semantic similarity (values from 0 to 2, where 0 is identical)
3. Metadata Storage: Points can store additional information (payload) alongside vectors
4. Filtering: Search results can be constrained using payload filters
5. Scoring: Results are returned with similarity scores (higher is more similar for cosine similarity)

Available Search Methods:
1. query_points() - Primary method for vector similarity search
2. query_batch_points() - Batch multiple queries for efficiency
3. search() - Legacy search method (not available in newer versions)
4. scroll() - Retrieve points by payload without similarity search
5. retrieve() - Get specific points by ID
6. count() - Count points matching filters
"""

# 1. BASIC QUERY_POINTS SEARCH
# The primary method for semantic similarity search
"""
qdrant_client.query_points(
    collection_name="your_collection",
    query=vector_list,                    # Vector to search for similar items
    limit=10,                           # Number of results to return
    with_payload=True,                  # Include metadata in results
    with_vectors=False,                 # Include vectors in results (True/False or list of names)
    query_filter=None,                  # Filter conditions (see filtering section)
    score_threshold=None,               # Minimum similarity score (0.0 to 1.0+)
    offset=None,                        # Skip first N results (for pagination)
    using=None,                         # Name of vector to use (for collections with multiple vectors)
    params=None,                        # Additional search parameters
    consistency=None,                   # Read consistency level
    shard_key_selector=None,            # Specify shards to search in
    timeout=None                        # Request timeout in seconds
)
"""

# 2. FILTERING OPTIONS
"""
Filters allow you to constrain search results based on payload (metadata) fields.

Basic filter structure:
filter = models.Filter(
    must=[...],        # All conditions must be true
    should=[...],      # At least one condition must be true
    must_not=[...],    # All conditions must be false
    min_should=None    # Minimum number of should conditions to match
)

Field conditions:
- models.FieldCondition(key="field_name", match=models.MatchValue(value="value"))
- models.FieldCondition(key="field_name", match=models.MatchText(text="text"))
- models.FieldCondition(key="field_name", range=models.Range(gte=0, lte=100))
- models.FieldCondition(key="field_name", geo_radius=models.GeoRadius(...))
"""

# 3. SEARCH PARAMETERS
"""
Search parameters can optimize the search algorithm:

params = models.SearchParams(
    hnsw_ef=128,           # Size of the beam in HNSW search (higher = more accurate, slower)
    exact=False,           # Exact search (slow but accurate)
    indexed_only=False,    # Only search indexed vectors (faster but less complete)
    quantization=None      # Quantization parameters for memory optimization
)
"""

# 4. COMPLETE SEARCH EXAMPLE
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Initialize client
client = QdrantClient(url="your-url", api_key="your-api-key")

# Example search with all options
results = client.query_points(
    collection_name="my_collection",
    query=[0.1, 0.2, 0.3, ...],  # Your query vector (same dimension as stored vectors)
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="technology")
            ),
            models.FieldCondition(
                key="date",
                range=models.Range(gte="2023-01-01")
            )
        ]
    ),
    limit=5,
    offset=0,
    with_payload=True,  # Return metadata
    with_vectors=False, # Don't return vectors to save bandwidth
    score_threshold=0.5,  # Only return results with similarity >= 0.5
    params=models.SearchParams(
        hnsw_ef=256,    # More accurate but slower search
        exact=False     # Use approximate search
    )
)

# Process results
for point in results.points:
    print(f"ID: {point.id}, Score: {point.score}, Payload: {point.payload}")
"""

# 5. BATCH SEARCH EXAMPLE
"""
# Perform multiple searches in one request for efficiency
search_requests = [
    models.QueryRequest(
        query=[0.1, 0.2, 0.3, ...],
        limit=5,
        with_payload=True
    ),
    models.QueryRequest(
        query=[0.4, 0.5, 0.6, ...],
        limit=5,
        with_payload=True
    )
]

batch_results = client.query_batch_points(
    collection_name="my_collection",
    requests=search_requests
)

# batch_results is a list of QueryResponse objects
for i, query_result in enumerate(batch_results):
    print(f"Results for query {i+1}:")
    for point in query_result.points:
        print(f"  ID: {point.id}, Score: {point.score}")
"""

# 6. PAGINATION EXAMPLE
"""
# For large result sets, use offset for pagination
all_results = []
offset = 0
limit = 10

while True:
    results = client.query_points(
        collection_name="my_collection",
        query=query_vector,
        limit=limit,
        offset=offset,
        with_payload=True
    )

    if not results.points:
        break  # No more results

    all_results.extend(results.points)
    offset += limit

    if len(results.points) < limit:
        break  # Last page
"""

# 7. FILTERING EXAMPLES
"""
# String equality filter
filter1 = models.Filter(
    must=[models.FieldCondition(
        key="title",
        match=models.MatchValue(value="Introduction to AI")
    )]
)

# Text search (for text fields)
filter2 = models.Filter(
    must=[models.FieldCondition(
        key="content",
        match=models.MatchText(text="machine learning")
    )]
)

# Numeric range filter
filter3 = models.Filter(
    must=[models.FieldCondition(
        key="word_count",
        range=models.Range(gte=100, lte=1000)
    )]
)

# Multiple conditions (AND)
filter4 = models.Filter(
    must=[
        models.FieldCondition(key="category", match=models.MatchValue(value="tech")),
        models.FieldCondition(key="published", range=models.Range(gte="2023-01-01"))
    ]
)

# OR conditions
filter5 = models.Filter(
    should=[
        models.FieldCondition(key="tag", match=models.MatchValue(value="AI")),
        models.FieldCondition(key="tag", match=models.MatchValue(value="ML"))
    ]
)

# NOT conditions
filter6 = models.Filter(
    must_not=[models.FieldCondition(
        key="status",
        match=models.MatchValue(value="archived")
    )]
)
"""

# 8. PAYLOAD RETRIEVAL OPTIONS
"""
# Retrieve all payload
with_payload=True

# Retrieve no payload
with_payload=False

# Retrieve specific payload fields only
with_payload=["title", "url", "author"]

# Complex payload selector
with_payload=models.PayloadSelectorInclude(include=["title", "url"])
"""

# 9. PERFORMANCE CONSIDERATIONS
"""
- Use score_threshold to limit results and improve performance
- Use indexed_only=True to search only indexed vectors (faster but less complete)
- Adjust hnsw_ef parameter: lower values = faster search, higher values = more accurate
- Use batch operations when performing multiple searches
- Consider using filters to reduce the search space
- For large collections, use pagination with offset
"""

# 10. ERROR HANDLING
"""
try:
    results = client.query_points(
        collection_name="my_collection",
        query=query_vector,
        limit=10,
        with_payload=True
    )
    # Process results
    for point in results.points:
        print(f"ID: {point.id}, Score: {point.score}")

except Exception as e:
    print(f"Search failed: {str(e)}")
    # Handle error appropriately
"""