<!--
Sync Impact Report:
- Version change: N/A -> 1.0.0
- Modified principles: N/A (initial creation)
- Added sections: All principles and sections as specified
- Removed sections: None
- Templates requiring updates: ✅ Updated all relevant templates
- Follow-up TODOs: None
-->
# Spec-Driven Technical Book with Embedded RAG Chatbot Constitution

## Core Principles

### I. Spec-First Authoring
All book content and RAG chatbot functionality must begin with a clearly defined specification. No implementation proceeds without an approved spec that defines scope, acceptance criteria, and technical requirements.

### II. Technical Accuracy and Reproducibility
All code examples, technical claims, and implementation details must be verified and reproducible. Every example must work as described, with clear setup and execution instructions.

### III. Strict RAG Grounding (NON-NEGOTIABLE)
The chatbot must only respond based on retrieved content from the book or user-selected text. Any query that cannot be answered from the provided context must result in a refusal response, never hallucination.

### IV. Separation of Content, AI, and Infrastructure
Book content, AI processing logic, and deployment infrastructure must be developed and maintained as distinct layers with well-defined interfaces between them.

### V. Deterministic Content Processing
Content ingestion, chunking, and embedding processes must be deterministic and reproducible to ensure consistent retrieval behavior across book versions.

### VI. Quality-Driven Publication Pipeline
All content must pass verification checks before publication. The RAG system must be validated against the published content to ensure accurate responses.

## Technology Stack Standards
- Book Platform: Docusaurus for documentation and publishing
- Hosting: GitHub Pages for static hosting
- AI Stack: OpenAI Agents/ChatKit, FastAPI, Neon Serverless Postgres, Qdrant Cloud
- Development Tools: Spec-Kit Plus, Claude Code for spec-driven development
- Content Format: Markdown files managed in Git repository

## Development Workflow
- All features must follow the spec-plan-tasks implementation cycle
- Book content must be reviewed for technical accuracy before merging
- RAG functionality must be tested with sample queries against actual book content
- Deployment pipeline must include content validation and RAG system health checks
- Versioning must align between book releases and RAG embeddings

## Governance
This constitution governs all development activities for the technical book and embedded RAG chatbot. All team members must comply with these principles. Changes to this constitution require explicit approval and documentation of the rationale. All pull requests must demonstrate compliance with these principles, particularly regarding technical accuracy, grounding requirements, and spec-first methodology.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
