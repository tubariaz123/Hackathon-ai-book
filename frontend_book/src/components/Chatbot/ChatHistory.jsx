import React from 'react';
import ChatMessage from './ChatMessage';

// ChatHistory component to display the conversation history
const ChatHistory = React.forwardRef(({ messages = [], showSources = true }, ref) => {
  return (
    <div className="chatbot-messages" role="log" aria-label="Chat conversation history">
      {messages.length === 0 ? (
        <div className="welcome-message" aria-label="Welcome message">
          <p>Hello! I'm your AI assistant for this book. Ask me anything about the content!</p>
        </div>
      ) : (
        <ul className="messages-list" aria-label="Message list">
          {messages.map((message) => (
            <li key={message.id} role="listitem">
              <ChatMessage
                message={message}
                showSources={showSources}
              />
            </li>
          ))}
        </ul>
      )}
      <div ref={ref} aria-hidden="true" />
    </div>
  );
});

ChatHistory.displayName = 'ChatHistory';

export default ChatHistory;