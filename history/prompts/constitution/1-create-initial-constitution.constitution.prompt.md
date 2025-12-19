---
id: 1
title: Create Initial Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,spec-first,rag,book]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
/sp.constitution

Project: Spec-Driven Technical Book with Embedded RAG Chatbot

Objective:
Author a technical book using Claude Code and Spec-Kit Plus, publish it with Docusaurus on GitHub Pages, and embed a RAG chatbot that answers questions strictly from the book content or user-selected text.

Core principles:
- Spec-first authoring
- Technical accuracy and reproducibility
- Strict grounding (no hallucinations)
- Clear separation of content, AI, and infrastructure

Book standards:
- Audience: software and AI engineers
- Tooling: Spec-Kit Plus, Claude Code
- Framework: Docusaurus
- Hosting: GitHub Pages
- All claims and examples must be verifiable
- No placeholders in final output

RAG chatbot standards:
- Stack: OpenAI Agents/ChatKit, FastAPI, Neon Serverless Postgres, Qdrant Cloud
- Answers must be derived only from retrieved book content
- Must support answering from full book or user-selected text
- Refuse answers when context is insufficient

Pipeline constraints:
- Ingest content directly from Docusaurus markdown
- Deterministic chunking and embeddings
- Version embeddings with book releases

Quality standards:
- Executable deployment steps
- Correct, documented code
- Grounded, traceable chatbot responses

Success criteria:
- Book live on GitHub Pages
- Embedded RAG chatbot operational
- Reproducible from repository alone
```

## Response snapshot

Created the initial project constitution file with the following principles:

1. Spec-First Authoring: All content and functionality must begin with a clearly defined specification
2. Technical Accuracy and Reproducibility: All examples and claims must be verified and reproducible
3. Strict RAG Grounding (NON-NEGOTIABLE): Chatbot must only respond based on retrieved content, never hallucinate
4. Separation of Content, AI, and Infrastructure: Distinct layers with well-defined interfaces
5. Deterministic Content Processing: Reproducible ingestion, chunking, and embedding
6. Quality-Driven Publication Pipeline: Content validation before publication

The constitution also includes Technology Stack Standards, Development Workflow, and Governance sections aligned with the project requirements.

## Outcome

- ✅ Impact: Created initial project constitution file with all required principles
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated with project-specific constitution
- 🔁 Next prompts: Proceed with feature specification using /sp.specify
- 🧠 Reflection: Constitution properly captures the core principles of spec-first development, technical accuracy, strict RAG grounding, and clear separation of concerns

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution properly implemented
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification phase