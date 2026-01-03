# Data Model: Frontend-Backend Integration for RAG Chatbot

## Frontend Data Models

### ChatMessage
- **id**: string (unique identifier for the message)
- **content**: string (the text content of the message)
- **sender**: enum ['user', 'agent'] (who sent the message)
- **timestamp**: datetime (when the message was created)
- **sources**: array of Source objects (for agent responses only)
- **confidence**: number (confidence level for agent responses)

### Source
- **title**: string (title of the source document)
- **url**: string (URL to the source)
- **snippet**: string (relevant text snippet)

### Conversation
- **id**: string (unique identifier for the conversation)
- **messages**: array of ChatMessage objects
- **createdAt**: datetime (when the conversation started)
- **updatedAt**: datetime (when the conversation was last updated)

## Backend API Models

### QueryRequest
- **query**: string (the user's question)
- **sessionId**: string (optional session identifier for conversation context)
- **maxResults**: number (optional, default 5, number of results to retrieve)

### QueryResponse
- **query**: string (echo of the original query)
- **answer**: string (the agent's response)
- **sources**: array of Source objects (source attribution)
- **confidence**: number (confidence score)
- **retrievedContextCount**: number (number of context items used)

## API Contract

### POST /query
- **Purpose**: Process a user query through the RAG agent
- **Request Body**: QueryRequest object
- **Response**: QueryResponse object
- **Error Responses**:
  - 400: Invalid request format
  - 422: Unprocessable query
  - 500: Internal server error

### GET /health
- **Purpose**: Check backend service health
- **Response**: Health status object