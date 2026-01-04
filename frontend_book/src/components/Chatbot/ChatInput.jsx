import React, { useState, useRef, useEffect } from 'react';
import { FiSend } from 'react-icons/fi';

// ChatInput component for user query input
const ChatInput = ({ onSendMessage, isLoading = false }) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');
  const textareaRef = useRef(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px';
    }
  }, [inputValue]);

  const validateInput = (value) => {
    if (!value.trim()) {
      setError('Query cannot be empty');
      return false;
    }

    if (value.trim().length < 3) {
      setError('Query must be at least 3 characters long');
      return false;
    }

    if (value.length > 1000) {
      setError('Query is too long (maximum 1000 characters)');
      return false;
    }

    setError('');
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateInput(inputValue) && !isLoading) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleChange = (e) => {
    const value = e.target.value;
    setInputValue(value);
    // Clear error when user starts typing
    if (error && value.trim()) {
      validateInput(value);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="chat-input-form">
      <textarea
        ref={textareaRef}
        value={inputValue}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about the book content..."
        className={`chat-input ${error ? 'input-error' : ''}`}
        disabled={isLoading}
        rows={1}
        aria-label="Type your question here"
        aria-invalid={!!error}
        aria-describedby={error ? "input-error-message" : undefined}
      />
      {error && (
        <div id="input-error-message" className="input-error-message" role="alert">
          {error}
        </div>
      )}
      <button
        type="submit"
        className="chat-submit-button"
        disabled={isLoading || !inputValue.trim() || !!error}
        aria-label="Send message"
      >
        <FiSend aria-hidden="true" />
      </button>
    </form>
  );
};

export default ChatInput;