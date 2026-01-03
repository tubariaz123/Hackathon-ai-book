# Research: Retrieval and pipeline validation

## Decision: Qdrant Connection Details
**Rationale**: Based on analysis of backend/src/main.py and backend/.env.example
**Findings**:
- Qdrant URL: Stored in QDRANT_URL environment variable (e.g., "https://410128ca-a093-4648-aabb-93bec0588715.us-east4-0.gcp.cloud.qdrant.io:6333")
- Qdrant API Key: Stored in QDRANT_API_KEY environment variable
- Client initialized with: `QdrantClient(url=qdrant_url, api_key=qdrant_api_key, timeout=60.0)`
- Connection uses HTTPS with API key authentication

## Decision: Qdrant Collection Name
**Rationale**: Based on analysis of backend/src/main.py
**Findings**:
- Collection name: "rag_embedding" (defined in main() function)
- Created with 1024-dimensional vectors using Cohere's embed-english-v3.0 model
- Uses cosine distance for similarity calculations
- Each point contains embedding vector and metadata payload

## Decision: Embedding Model Compatibility
**Rationale**: Based on analysis of backend/src/main.py
**Findings**:
- Embedding model: Cohere's "embed-english-v3.0"
- Vector dimensions: 1024 (for input_type="search_document")
- Input type: "search_document" (appropriate for document search)
- For retrieval, the same model must be used to embed query text as was used for the stored vectors

## Decision: Top-K Value
**Rationale**: Based on best practices for retrieval validation
**Findings**:
- Default top-k: 5 (common for retrieval validation)
- Configurable parameter to allow testing different result set sizes
- Top-k=5 aligns with the success criteria in the spec (top 5 results)

## Decision: Qdrant Search Method
**Rationale**: Based on Qdrant Python client API documentation
**Findings**:
- Primary search method: `qdrant_client.search()` for semantic similarity
- Parameters needed: collection_name, query_vector, limit (top-k), with_payload=True
- Query vector must match the stored vector dimensions (1024)
- with_payload=True ensures metadata is returned with results
- Example: `qdrant_client.search(collection_name="rag_embedding", query_vector=query_embedding, limit=5, with_payload=True)`

## Decision: Validation Approaches
**Rationale**: Based on the success criteria in the feature specification
**Findings**:
- Relevance validation: Compare semantic similarity scores and content relevance
- Stability validation: Execute same query multiple times and verify consistent results
- Metadata validation: Ensure all expected metadata fields are returned
- Performance validation: Measure response times and consistency across runs
- Test framework: Create repeatable test suite that runs queries and validates outputs

## Alternatives Considered:
1. For search methods: Considered various Qdrant client methods but settled on search() as the primary semantic similarity method
2. For validation: Considered different metrics but focused on relevance scores and result consistency as per spec
3. For top-k: Considered various values but 5 is standard for retrieval evaluation and matches spec requirements