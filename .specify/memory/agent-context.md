# AI Book Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-25

## Active Technologies

- Python 3.x backend
- Qdrant vector database (cloud instance)
- Cohere API for embeddings (embed-english-v3.0 model)
- Python-dotenv for environment management
- Requests for HTTP operations
- BeautifulSoup for HTML parsing
- Docusaurus for frontend documentation

## Project Structure

```text
backend/
├── retrieve.py (new: semantic retrieval and validation module)
├── src/
│   └── main.py (URL ingestion, text extraction, embedding, storage)
├── requirements.txt
├── .env.example
└── .env
specs/006-retrieval-validation/
├── spec.md
├── plan.md
├── research.md
└── checklists/
frontend_book/ (Docusaurus documentation site)
history/prompts/ (Prompt History Records)
```

## Commands

- `python backend/src/main.py` - Run the URL ingestion pipeline
- `python -m backend.retrieve` - Run the retrieval validation module
- `pip install -r backend/requirements.txt` - Install backend dependencies
- Environment variables: QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY

## Code Style

- Python: Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Include docstrings for all functions and classes
- Use logging instead of print statements
- Handle exceptions appropriately
- Use environment variables for configuration

## Recent Changes

- Retrieval and pipeline validation: Added semantic retrieval module with validation capabilities
- URL ingestion: Added web crawling, text extraction, chunking, and embedding storage
- RAG system: Established vector database infrastructure with Qdrant and Cohere embeddings

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->