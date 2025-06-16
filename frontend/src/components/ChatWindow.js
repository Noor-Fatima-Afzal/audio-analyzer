import React, { useState, useRef, useEffect } from 'react';
import './ChatWindow.css';
import { IoSend } from "react-icons/io5";

function ChatWindow() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false); 
  const chatEndRef = useRef(null); 

  const handleSendMessage = async () => {
    if (message.trim()) {
      const newMessage = { sender: 'user', text: message };
      setChatHistory(prev => [...prev, newMessage]);

      // Set loading state to true
      setIsLoading(true);

      try {
        const response = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message }),
        });
        const data = await response.json();

        // Create bot response message
        const botResponse = { sender: 'bot', text: data.response };
        setChatHistory(prev => [...prev, botResponse]);
      } catch (error) {
        console.error("Error fetching bot response:", error);
      } finally {
        // Reset the loading state
        setIsLoading(false);
      }

      setMessage(''); // Clear the input field
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  // Scroll to the bottom whenever chatHistory changes
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory]);

  return (
    <div className="chat-window">
      <h2>Chat with us</h2>
      <div className="chat-content">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="chat-message bot">
            .... 
          </div>
        )}
        {/* Add an empty div to act as a scroll target */}
        <div ref={chatEndRef} />
      </div>
      <div className="chat-input-container">
        <input
          className="chat-input"
          type="text"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress} // Add key press handler
        />
        <button className="send-button" onClick={handleSendMessage}>
          <IoSend />
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
