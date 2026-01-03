# Implementation Plan: URL Ingestion, Embeddings, and Vector Storage

**Branch**: `005-url-ingestion` | **Date**: 2025-12-20 | **Spec**: specs/005-url-ingestion/spec.md
**Input**: Feature specification from `/specs/005-url-ingestion/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a single-file backend service in main.py that crawls the deployed Docusaurus book at https://hackathon-ai-book-fawn.vercel.app/, extracts text content, chunks it, generates Cohere embeddings, and stores vectors with metadata in Qdrant. The system will include functions for URL crawling, text extraction, chunking, embedding, and vector storage.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: requests, beautifulsoup4, cohere, qdrant-client, python-dotenv
**Storage**: Qdrant vector database (external)
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Single-file backend service (main.py)
**Performance Goals**: Process book content efficiently with reasonable API response times
**Constraints**: Must handle Cohere API rate limits, network timeouts, and ensure 99.9% vector storage success
**Scale/Scope**: Support the deployed book at https://hackathon-ai-book-fawn.vercel.app/
**SiteMap URL**: Support the deployed book at https://hackathon-ai-book-fawn.vercel.app/sitemap.xml

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Spec-First Authoring**: ✅ Specification exists at specs/005-url-ingestion/spec.md
- **Technical Accuracy and Reproducibility**: ✅ Plan includes verification steps for each component
- **Strict RAG Grounding**: ✅ Implementation focuses on proper content ingestion for RAG
- **Separation of Content, AI, and Infrastructure**: ✅ Clear separation between crawling, embedding, and storage layers (within single file)
- **Deterministic Content Processing**: ✅ Plan includes consistent chunking and embedding processes
- **Quality-Driven Publication Pipeline**: ✅ Includes validation of successful storage and retrieval

## Project Structure

### Documentation (this feature)

```text
specs/005-url-ingestion/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   └── main.py          # Single-file implementation with all required functions
├── tests/
│   └── test_main.py     # Tests for the main functionality
├── requirements.txt
├── pyproject.toml
└── .env.example
```

**Structure Decision**: Single-file structure selected as requested, containing all functionality in main.py with functions: get_all_urls, extract_text_from_url, chunk_text, embed, create_collection named rag_embedding, save_chunk_to_qdrant, and main execution function.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |