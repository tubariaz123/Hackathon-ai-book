# Quickstart: URL Ingestion, Embeddings, and Vector Storage

## Prerequisites

- Python 3.11+
- `uv` package manager (or pip)
- Cohere API key
- Qdrant API key and endpoint

## Setup

1. **Create the backend directory and initialize the project:**

```bash
mkdir backend
cd backend
uv venv  # or python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**

```bash
uv pip install requests beautifulsoup4 cohere qdrant-client python-dotenv
```

Or create a requirements.txt:

```txt
requests==2.31.0
beautifulsoup4==4.12.2
cohere==4.4.3
qdrant-client==1.7.0
python-dotenv==1.0.0
```

3. **Set up environment variables:**

Create a `.env` file with the following content:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
ROOT_URL=https://hackathon-ai-book-fawn.vercel.app/
```

## Usage

1. **Run the ingestion process:**

```bash
cd backend
python src/main.py
```

This will:
- Crawl all pages from the specified Docusaurus book URL
- Extract text content from each page
- Chunk the content into appropriate sizes
- Generate embeddings using Cohere
- Store the vectors in Qdrant with metadata

## Configuration

The system can be configured via environment variables:

- `ROOT_URL`: The root URL of the Docusaurus book to crawl
- `CHUNK_SIZE`: Size of text chunks (default: 512 tokens)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 tokens)
- `COHERE_MODEL`: Cohere model to use for embeddings (default: embed-english-v3.0)