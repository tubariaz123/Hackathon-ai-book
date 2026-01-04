import React from 'react';
import Chatbot from './Chatbot';

// Example usage component for the Chatbot
const ExampleUsage = () => {
  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1>AI Book Assistant Demo</h1>
      <p>This is a demonstration of the integrated RAG chatbot component.</p>
      <p>Ask questions about the book content and receive grounded responses with source attribution.</p>

      <div style={{ marginTop: '20px', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' }}>
        <Chatbot />
      </div>

      <div style={{ marginTop: '20px', fontSize: '0.9rem', color: '#64748b' }}>
        <p><strong>Note:</strong> This chatbot connects to a backend RAG agent service that has been trained on book content.</p>
        <p>Responses are grounded in the source material and include citations to relevant sections.</p>
      </div>
    </div>
  );
};

export default ExampleUsage;