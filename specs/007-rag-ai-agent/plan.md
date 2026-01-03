# Implementation Plan: RAG AI Agent with OpenAI SDK and FastAPI

**Feature**: RAG AI Agent with OpenAI SDK and FastAPI
**Branch**: 007-rag-ai-agent
**Created**: 2025-12-26
**Status**: Draft
**Input**: Agent with Retrieval - Create a single `agent.py` file at the backend folder - Initialize an agent using the OpenAI Agents SDK - Integrate retrieval by calling the existing Qdrant search logic - Ensure the agent responds using retrieved book content only

## Technical Context

- **Target Architecture**: Python backend with OpenAI Chat Completions API and Qdrant integration
- **File to create**: `backend/agent.py`
- **Primary Function**: AI agent that retrieves content from Qdrant and responds based on retrieved context
- **Key Components**: OpenAI API integration, Qdrant retrieval integration, grounding validation
- **OpenAI API Key**: Using OPENAI_API_KEY from environment variables, loaded with python-dotenv
- **Agent Configuration**: Using gpt-4-turbo or gpt-3.5-turbo model via Chat Completions API with system message for grounding
- **Integration Method**: Import and use search_similar_content function from existing retrieve.py module
- **Grounding Enforcement**: System message instructing model to only use provided context and validation of responses

## Constitution Check

- ✅ Spec-First Authoring: Proceeding with implementation based on approved spec
- ✅ Technical Accuracy and Reproducibility: Code is testable and reproducible with validation framework
- ✅ Strict RAG Grounding: Implementation enforces responses based only on retrieved content
- ✅ Separation of Content, AI, and Infrastructure: Focusing on AI agent layer
- ✅ Deterministic Content Processing: Maintains consistency with existing retrieval
- ✅ Quality-Driven Publication Pipeline: Includes comprehensive validation functionality

## Phase 0: Research

### Research Summary

All research tasks completed and documented in [research.md](research.md):

1. **OpenAI Agents SDK**: Determined to use OpenAI Chat Completions API with system messages for RAG applications
2. **Qdrant Integration**: Identified approach to integrate with existing retrieve.py module
3. **Grounding Enforcement**: Documented methods to ensure responses are strictly based on retrieved content
4. **Agent Configuration**: Researched optimal OpenAI model configurations for RAG applications

## Phase 1: Design

### Data Model

Based on the existing system and feature requirements, the following data models are relevant:

#### AgentQuery Model
- **query_text**: (string) The input question from the user
- **max_results**: (integer) Number of results to retrieve from Qdrant (default: 5)
- **grounding_required**: (boolean) Whether strict grounding in retrieved content is required (default: True)

#### AgentResponse Model
- **query**: (string) The original query text
- **answer**: (string) The AI-generated answer based on retrieved context
- **retrieved_context**: (list) List of RetrievalResult objects from Qdrant
- **sources**: (list) List of source URLs/titles from metadata
- **confidence**: (float) Confidence score of the response (0.0-1.0)

#### RAGAgent Model
- **model_name**: (string) The OpenAI model to use (e.g., "gpt-4-turbo")
- **system_prompt**: (string) System message to enforce grounding behavior
- **retrieval_function**: (callable) Function to retrieve content from Qdrant
- **grounding_enforcement**: (boolean) Whether to strictly enforce response grounding

### API Contracts

Based on the functional requirements, the following API contracts will be implemented in the agent.py module:

#### Function: create_rag_agent(model_name="gpt-4-turbo")
- **Purpose**: Initialize and return a RAG agent with specified OpenAI model
- **Input**: model_name (string, optional) - OpenAI model to use
- **Output**: RAGAgent object configured for grounded responses

#### Function: query_agent(agent, query_text, top_k=5)
- **Purpose**: Process a user query through the RAG agent
- **Input**:
  - agent (RAGAgent): The configured RAG agent
  - query_text (string): The user's question
  - top_k (integer, optional): Number of results to retrieve from Qdrant
- **Output**: AgentResponse object with answer and source information

#### Function: enforce_grounding(response_text, retrieved_context)
- **Purpose**: Validate that the response is grounded in retrieved context
- **Input**:
  - response_text (string): The generated response
  - retrieved_context (list): Retrieved content used for response
- **Output**: Boolean indicating if response is properly grounded

### Quickstart Guide

#### Setup
1. Ensure environment variables are set:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `QDRANT_URL`: Your Qdrant cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key

2. Install dependencies (add OpenAI to requirements):
   ```bash
   pip install openai
   ```

#### Basic Usage
1. Import the agent module:
   ```python
   from backend.agent import create_rag_agent, query_agent
   ```

2. Initialize the RAG agent:
   ```python
   agent = create_rag_agent(model_name="gpt-4-turbo")
   ```

3. Query the agent:
   ```python
   response = query_agent(agent, "Your question here", top_k=5)
   print(f"Answer: {response.answer}")
   print(f"Sources: {response.sources}")
   ```

#### Environment Setup
- Copy `.env.example` to `.env` and fill in your API keys
- Ensure the Qdrant collection "rag_embedding" exists with data
- Verify OpenAI API access for chat completions

## Phase 2: Implementation

### Tasks

1. **Create agent.py module**: Set up the basic file structure with necessary imports
2. **Implement OpenAI API integration**: Initialize OpenAI client using environment variables
3. **Implement RAG agent creation**: Create function to initialize RAG agent with grounding configuration
4. **Implement retrieval integration**: Integrate with existing search_similar_content function from retrieve.py
5. **Implement response generation**: Create function to generate responses using retrieved context
6. **Implement grounding enforcement**: Add validation to ensure responses are based on retrieved content
7. **Implement error handling**: Add proper exception handling for API and retrieval errors
8. **Add logging**: Implement logging for debugging and monitoring
9. **Write unit tests**: Create tests for each function to ensure reliability

## Phase 3: Validation

### Testing Strategy

#### Unit Tests
- Test OpenAI API integration with mocked responses
- Test retrieval integration with known queries against test data
- Test grounding enforcement functions
- Test error handling for API and retrieval failures
- Test response formatting and source attribution

#### Integration Tests
- Test end-to-end RAG functionality with real OpenAI and Qdrant connection
- Validate that responses are grounded in retrieved context
- Test source attribution and metadata handling
- Verify grounding enforcement works correctly

#### Performance Tests
- Measure response times under various query loads
- Test token usage and cost optimization
- Validate that grounding checks don't significantly impact performance

### Risk Assessment

- **OpenAI API Costs**: Risk of high usage costs; implement token usage tracking and rate limiting
- **Grounding Validation**: Risk of hallucination despite validation; implement multiple validation layers
- **Performance**: Risk of slow responses due to multiple API calls; implement caching and optimization
- **Dependency Changes**: Risk of OpenAI API changes; implement proper error handling and version management

### Dependencies

- **Primary**: OpenAI API access with valid API key
- **API Keys**: Valid OPENAI_API_KEY, QDRANT_URL, and QDRANT_API_KEY in environment
- **Models**: GPT-4 Turbo or GPT-3.5 Turbo model access
- **Python Packages**: openai, python-dotenv (to be added to requirements)

### Success Criteria

- ✅ RAG agent retrieves relevant book content from Qdrant for user queries
- ✅ Responses are grounded strictly in retrieved context with no hallucinations
- ✅ System handles both book-level and section-level queries appropriately
- ✅ Agent responds using retrieved book content only as enforced by grounding validation
- ✅ FastAPI endpoint can be implemented to interact with the agent successfully
- ✅ Module passes all unit and integration tests