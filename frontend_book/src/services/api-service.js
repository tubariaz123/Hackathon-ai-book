import axios from 'axios';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Default backend URL
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Error handling utilities
const handleApiError = (error) => {
  // Log error for debugging purposes
  console.error('API Error:', error);

  if (error.response) {
    // Server responded with error status
    const status = error.response.status;
    const message = error.response.data?.detail || error.response.data?.message || 'Unknown error';

    // Log specific error details
    console.error(`API Response Error ${status}:`, error.response.data);

    switch (status) {
      case 400:
        return new Error(`Bad Request: ${message}`);
      case 422:
        return new Error(`Unprocessable Query: ${message}`);
      case 500:
        return new Error(`Internal Server Error: ${message}`);
      default:
        return new Error(`Backend error: ${status} - ${message}`);
    }
  } else if (error.request) {
    // Request was made but no response received
    console.error('Network Error:', error.request);
    return new Error('Network error: Unable to reach the backend service');
  } else {
    // Something else happened
    console.error('Request Error:', error.message);
    return new Error(`Request error: ${error.message}`);
  }
};

// Logging utility for API calls
const logApiCall = (endpoint, method = 'GET', data = null) => {
  console.log(`API Call: ${method} ${endpoint}`, data ? { data } : {});
};

// API service functions
const apiService = {
  // Query the RAG agent
  query: async (queryData) => {
    // Map field names to match the backend API contract
    // Convert camelCase to snake_case to match backend expectations
    const requestData = {
      query_text: queryData.query || queryData.query_text,
      session_id: queryData.sessionId || queryData.session_id,
      max_results: queryData.maxResults || queryData.max_results || 5,
      grounding_required: queryData.groundingRequired || queryData.grounding_required || true,
      model_name: queryData.modelName || queryData.model_name || "gpt-4-turbo"
    };

    // Log the API call for debugging
    logApiCall('/query', 'POST', requestData);

    try {
      const response = await apiClient.post('/query', requestData);
      // Ensure response fields match the expected format
      return {
        query: response.data.query,
        answer: response.data.answer,
        sources: response.data.sources,
        confidence: response.data.confidence,
        retrievedContextCount: response.data.retrieved_context_count || response.data.retrievedContextCount
      };
    } catch (error) {
      throw handleApiError(error);
    }
  },

  // Health check for the backend service
  healthCheck: async () => {
    // Log the API call for debugging
    logApiCall('/health', 'GET');

    try {
      const response = await apiClient.get('/health');
      // Ensure response fields match the expected HealthResponse format
      return {
        status: response.data.status,
        message: response.data.message
      };
    } catch (error) {
      throw handleApiError(error);
    }
  }
};

export default apiService;