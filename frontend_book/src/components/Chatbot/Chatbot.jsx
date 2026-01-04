import React, { useState, useEffect, useCallback, useRef } from 'react';
import ChatHistory from './ChatHistory';
import ChatInput from './ChatInput';
import apiService from '../../services/api-service';
import '../../../static/chatbot-styles.css';

// Base Chatbot component structure
const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const abortControllerRef = useRef(null);

  // Generate a unique session ID if one doesn't exist
  useEffect(() => {
    if (!sessionId) {
      // Create a simple session ID based on timestamp and random number
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(newSessionId);
    }
  }, [sessionId]);

  // Scroll to the bottom of the chat when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Cleanup function to prevent memory leaks
  useEffect(() => {
    return () => {
      // Abort any ongoing requests when component unmounts
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  // Initialize the chatbot
  useEffect(() => {
    // Optionally check backend health on component mount
    const initializeChatbot = async () => {
      try {
        await apiService.healthCheck();
      } catch (err) {
        console.warn('Backend health check failed:', err.message);
        // Continue anyway, as backend might still be starting up
      }
    };

    initializeChatbot();
  }, []);

  // Function to handle sending a message
  const handleSendMessage = async (queryText) => {
    if (!queryText.trim() || isLoading) return;

    // Cancel any previous ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new AbortController for this request
    abortControllerRef.current = new AbortController();

    // Create user message object
    const userMessage = {
      id: Date.now().toString(),
      content: queryText,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    // Add user message to the conversation
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Prepare query data with session information
      const queryData = {
        query_text: queryText,
        session_id: sessionId,
        max_results: 5,
        grounding_required: true,
        model_name: "gpt-4-turbo"
      };

      // Send query to backend
      const response = await apiService.query(queryData);

      // Create agent response message
      const agentMessage = {
        id: `agent-${Date.now()}`,
        content: response.answer,
        sender: 'agent',
        timestamp: new Date().toISOString(),
        sources: response.sources,
        confidence: response.confidence,
      };

      // Add agent response to the conversation
      setMessages(prev => [...prev, agentMessage]);
    } catch (err) {
      // Check if the error is due to request cancellation
      if (err.name === 'AbortError') {
        // Request was cancelled, don't show error message
        return;
      }

      // Create user-friendly error message
      let userFriendlyMessage = "Sorry, I encountered an issue processing your request. Please try again.";

      // Provide more specific messages based on error type
      if (err.message.includes('Network error')) {
        userFriendlyMessage = "Unable to connect to the AI service. Please check your internet connection and try again.";
      } else if (err.message.includes('Backend error')) {
        userFriendlyMessage = "The AI service is temporarily unavailable. Please try again in a moment.";
      } else if (err.message.includes('Bad Request')) {
        userFriendlyMessage = "Your query couldn't be processed. Please try rephrasing your question.";
      } else if (err.message.includes('Unprocessable Query')) {
        userFriendlyMessage = "I couldn't find relevant information to answer your question. Please try asking differently.";
      } else if (err.message.includes('Internal Server Error')) {
        userFriendlyMessage = "An error occurred on our end. Please try again later.";
      } else if (err.message.includes('Health check failed')) {
        userFriendlyMessage = "The AI service is not available right now. Please try again later.";
      }

      const errorMessage = {
        id: `error-${Date.now()}`,
        content: userFriendlyMessage,
        sender: 'agent',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
      setError(userFriendlyMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatbot-container" role="main" aria-label="AI Book Assistant Chat Interface">
      <div className="chatbot-header" aria-live="polite" aria-atomic="true">
        AI Book Assistant
      </div>

      <ChatHistory
        messages={messages}
        ref={messagesEndRef}
        aria-live="polite"
        aria-relevant="additions"
      />

      <div className="chat-input-container" role="form" aria-label="Chat input area">
        <ChatInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>

      {isLoading && (
        <div className="loading-indicator" aria-label="Loading, please wait" aria-live="polite">
          <div className="typing-indicator" role="status" aria-label="Assistant is typing">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;