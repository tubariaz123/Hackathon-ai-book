# Quickstart: Frontend-Backend Integration for RAG Chatbot

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend services
- Docusaurus project set up in `frontend_book/`
- FastAPI backend running in `backend/`
- OpenAI API key configured in environment

## Setup

### 1. Clone and Initialize
```bash
# Navigate to the project directory
cd ai-book

# Install frontend dependencies
cd frontend_book
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Create backend environment file
cd backend
cp .env.example .env
# Edit .env to include your OpenAI API key and other required variables
```

### 3. Start Backend Service
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Start Frontend Development Server
```bash
cd frontend_book
npm start
```

## Usage

### 1. Integrate Chatbot Component
Add the chatbot component to your Docusaurus pages:

```jsx
// In your Docusaurus page
import Chatbot from '@site/src/components/Chatbot';

function MyPage() {
  return (
    <Layout>
      <div className="container">
        {/* Your page content */}
      </div>
      <Chatbot />
    </Layout>
  );
}
```

### 2. Making API Calls
The chatbot component will automatically handle API communication with the backend:

- Queries are sent to `POST /query`
- Responses include source attribution and confidence scores
- Error handling is built into the component

### 3. Testing the Integration
1. Visit your Docusaurus site in the browser
2. Use the embedded chatbot to ask questions about the book content
3. Verify that responses are grounded in the book content with proper source attribution
4. Check that conversation context is maintained across multiple exchanges

## API Endpoints

### Query Endpoint
- **URL**: `http://localhost:8000/query` (or your backend URL)
- **Method**: POST
- **Request Body**: `{"query_text": "your question here"}`
- **Response**: Grounded answer with sources and confidence score

### Health Check
- **URL**: `http://localhost:8000/health`
- **Method**: GET
- **Response**: Health status of the backend service

## Troubleshooting

### Common Issues
- **Backend not responding**: Verify backend service is running and URL is correct
- **CORS errors**: Ensure backend allows requests from frontend origin
- **API key errors**: Check that OpenAI API key is correctly configured
- **No responses**: Verify that the RAG system has been properly initialized with book content

### Verification Steps
1. Test backend directly with curl:
   ```bash
   curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query_text": "What is this book about?"}'
   ```
2. Check browser console for frontend errors
3. Verify environment variables are properly set