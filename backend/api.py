"""
FastAPI endpoints for the RAG AI Agent.

This module provides API endpoints for:
- Processing user queries through the RAG agent
- Returning grounded responses based on retrieved content
- Handling request/response validation
"""
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import logging
from backend.agent import create_rag_agent, query_agent, AgentQuery, AgentResponse, RAGAgent


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG AI Agent API", version="1.0.0")


# Pydantic models for API requests and responses
class QueryRequest(BaseModel):
    """Request model for agent queries."""
    query_text: str = Field(..., min_length=1, max_length=1000, description="The question to ask the agent")
    max_results: int = Field(default=5, ge=1, le=20, description="Number of results to retrieve from Qdrant")
    grounding_required: bool = Field(default=True, description="Whether strict grounding in retrieved content is required")
    model_name: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use for the agent")


class QueryResponse(BaseModel):
    """Response model for agent queries."""
    query: str
    answer: str
    sources: List[str]
    confidence: float
    retrieved_context_count: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str


# Global agent instance (in production, you might want to implement a more sophisticated agent management)
agent: Optional[RAGAgent] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent on startup."""
    global agent
    try:
        logger.info("Initializing RAG agent on startup...")
        agent = create_rag_agent(model_name="gpt-3.5-turbo")
        logger.info("RAG agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG agent: {str(e)}")
        raise


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", message="RAG AI Agent API is running")


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query through the RAG agent.

    Args:
        request: QueryRequest containing the query text and parameters

    Returns:
        QueryResponse with the answer and source information
    """
    global agent

    try:
        logger.info(f"Processing query: '{request.query_text[:50]}...'")

        # Validate that the agent is initialized
        if agent is None:
            raise HTTPException(status_code=503, detail="RAG agent not initialized")

        # Check if we need to recreate the agent with a different model
        if agent.model_name != request.model_name:
            logger.info(f"Switching agent model from {agent.model_name} to {request.model_name}")
            agent = create_rag_agent(model_name=request.model_name)

        # Process the query using the agent
        response = query_agent(
            agent=agent,
            query_text=request.query_text,
            top_k=request.max_results
        )

        # Update grounding enforcement based on request
        if request.grounding_required != agent.grounding_enforcement:
            agent.grounding_enforcement = request.grounding_required

        logger.info(f"Successfully processed query: '{request.query_text[:50]}...'")

        return QueryResponse(
            query=response.query,
            answer=response.answer,
            sources=response.sources,
            confidence=response.confidence,
            retrieved_context_count=len(response.retrieved_context)
        )

    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/models")
async def list_models():
    """
    List available models for the RAG agent.

    Returns:
        List of available model names
    """
    available_models = ["gpt-3.5-turbo", "gpt-3.5-turbo"]
    return {"models": available_models}


@app.post("/query_simple")
async def process_simple_query(query_text: str):
    """
    Simple query endpoint for basic usage.

    Args:
        query_text: The question to ask the agent

    Returns:
        The answer from the agent
    """
    global agent

    if not query_text or len(query_text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query text cannot be empty")

    if agent is None:
        raise HTTPException(status_code=503, detail="RAG agent not initialized")

    try:
        response = query_agent(agent=agent, query_text=query_text, top_k=5)
        return {"answer": response.answer, "sources": response.sources}
    except Exception as e:
        logger.error(f"Error processing simple query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)