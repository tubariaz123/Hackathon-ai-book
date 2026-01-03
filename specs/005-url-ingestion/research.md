# Research: URL Ingestion, Embeddings, and Vector Storage

## Decision: Project Structure
**Rationale**: User specifically requested a single-file implementation in main.py with all functionality contained in that file. This simplifies the initial implementation and makes it easier to understand the complete workflow in one place.

**Alternatives considered**:
- Multi-file structure with separate modules for crawling, embedding, and storage
- Full backend service with API endpoints
- CLI tool approach

## Decision: Dependencies
**Rationale**: Using requests for HTTP requests, beautifulsoup4 for HTML parsing, cohere for embeddings, and qdrant-client for vector storage are the standard libraries for these tasks in Python.

**Alternatives considered**:
- Using scrapy instead of requests/beautifulsoup4 for crawling (more complex than needed)
- Using OpenAI embeddings instead of Cohere (user specifically requested Cohere)
- Using different vector databases like Pinecone or Weaviate (user specifically requested Qdrant)

## Decision: URL Crawling Approach
**Rationale**: For Docusaurus sites, we can either parse the sitemap.xml or recursively crawl from the root URL. Given the user wants to crawl https://hackathon-ai-book-fawn.vercel.app/, we'll implement a breadth-first crawl with proper URL filtering to stay within the domain.

**Alternatives considered**:
- Sitemap parsing (may not include all pages)
- Headless browser automation (unnecessary complexity)
- API-based crawling if available (not applicable for static Docusaurus sites)

## Decision: Text Chunking Strategy
**Rationale**: Using a sliding window approach with overlap to maintain context while ensuring chunks fit within Cohere's token limits. A common approach is 512 tokens with 10% overlap.

**Alternatives considered**:
- Fixed character length chunks (may break context)
- Sentence-boundary aware chunking (more complex but preserves meaning better)
- Semantic chunking (requires additional processing)

## Decision: Qdrant Collection Design
**Rationale**: Creating a collection named "rag_embedding" with appropriate vector dimensions for Cohere embeddings (1024 dimensions for most Cohere models) and metadata fields to store source URL, content, and other relevant information.

**Alternatives considered**:
- Different collection naming conventions
- Different vector dimensions (must match embedding model)
- Different metadata storage strategies