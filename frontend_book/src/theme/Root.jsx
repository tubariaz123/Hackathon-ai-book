import React from 'react';
import FloatingChatbot from '../components/FloatingChatbot/FloatingChatbot';

// Root component that wraps the entire application
const Root = ({ children }) => {
  return (
    <>
      {children}
      <FloatingChatbot />
    </>
  );
};

export default Root;