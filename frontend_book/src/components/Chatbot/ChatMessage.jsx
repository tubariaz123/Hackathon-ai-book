import React from 'react';
import { FiLink } from 'react-icons/fi';

// ChatMessage component to display individual messages
const ChatMessage = ({ message, showSources = true }) => {
  const { id, content, sender, timestamp, sources, confidence } = message;

  // Format timestamp for display
  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Get CSS class based on confidence level
  const getConfidenceClass = (confidence) => {
    if (confidence >= 0.8) return 'high-confidence';
    if (confidence >= 0.6) return 'medium-confidence';
    if (confidence >= 0.4) return 'low-confidence';
    return 'very-low-confidence';
  };

  return (
    <div
      className={`chat-message ${sender === 'user' ? 'message-user' : 'message-agent'}`}
      key={id}
      role="article"
      aria-label={`${sender} message`}
      tabIndex={0}
    >
      <div className="message-content">
        {content}

        {/* Source attribution for agent responses */}
        {sender === 'agent' && showSources && sources && sources.length > 0 && (
          <div className="source-attribution" role="region" aria-label="Sources">
            <strong>Sources:</strong>
            <ul className="source-list" aria-label="Source list">
              {sources.map((source, index) => {
                // Handle source based on data model - could be string or object
                let title, url, snippet;

                if (typeof source === 'string') {
                  // Handle string format "Title (URL)" or just URL
                  const sourceMatch = source.match(/^(.+?)\s*\((https?:\/\/[^\)]+)\)$/);
                  if (sourceMatch) {
                    title = sourceMatch[1];
                    url = sourceMatch[2];
                  } else {
                    title = source;
                  }
                } else if (typeof source === 'object' && source !== null) {
                  // Handle object format according to data model
                  title = source.title || source.name || 'Unknown Source';
                  url = source.url;
                  snippet = source.snippet;
                } else {
                  title = String(source);
                }

                return (
                  <li key={index} className="source-item">
                    {url ? (
                      <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-link"
                        aria-label={`Source link: ${title}`}
                      >
                        {title} <FiLink size={12} />
                      </a>
                    ) : (
                      <span>{title}</span>
                    )}
                    {snippet && (
                      <div className="source-snippet" aria-label="Source snippet">
                        <small>"{snippet}"</small>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        {/* Confidence indicator for agent responses */}
        {sender === 'agent' && confidence !== undefined && (
          <div className="confidence-indicator" aria-label="Response confidence">
            <span
              className={`confidence-score ${getConfidenceClass(confidence)}`}
              aria-label={`Confidence level: ${(confidence * 100).toFixed(1)}%`}
            >
              Confidence: {(confidence * 100).toFixed(1)}%
            </span>
          </div>
        )}
      </div>

      {timestamp && (
        <div className="message-timestamp" aria-label={`Message time: ${formatTime(timestamp)}`}>
          {formatTime(timestamp)}
        </div>
      )}
    </div>
  );
};

export default ChatMessage;