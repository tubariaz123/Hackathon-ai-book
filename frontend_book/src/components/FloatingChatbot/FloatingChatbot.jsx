import React, { useState, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import Chatbot from '../Chatbot/Chatbot';
import '../../../static/chatbot-styles.css';
import './floating-chatbot.css';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  // Close chatbot when navigating to a different page (optional behavior)
  useEffect(() => {
    setIsOpen(false);
  }, [location.pathname]);

  return (
    <>
      {isOpen && (
        <div className="floating-chatbot-overlay">
          <div className="floating-chatbot-container">
            <div className="floating-chatbot-header">
              <h3>AI Book Assistant</h3>
              <button
                className="floating-chatbot-close"
                onClick={toggleChatbot}
                aria-label="Close chatbot"
              >
                ×
              </button>
            </div>
            <div className="floating-chatbot-content">
              <Chatbot />
            </div>
          </div>
        </div>
      )}
      <button
        className={`floating-chatbot-button ${isOpen ? 'hidden' : ''}`}
        onClick={toggleChatbot}
        aria-label="Open AI Book Assistant"
      >
        🤖
      </button>
    </>
  );
};

export default FloatingChatbot;