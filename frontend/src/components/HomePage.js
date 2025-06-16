// HomePage.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import NavBar from './NavBar'; 
import Footer from './Footer'; 
import FeaturesSection from './FeaturesSection';
import TestimonialSection from './TestimonialSection'; 
import ChatWindow from './ChatWindow'; // Import the ChatWindow component
import './HomePage.css';         
import signalImage from '../assets/signal-image.png';
import SimulatedWaveform from './SimulatedWaveform';
import { BsFillChatTextFill } from "react-icons/bs";

function HomePage() {
  const [message, setMessage] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false); // State to manage chat window visibility

  useEffect(() => {
    // Fetch message from backend
    axios.get('http://localhost:5000/')
      .then(response => {
        setMessage(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching data!", error);
      });
  }, []);

  const toggleChatWindow = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <div className="homepage-container">
      <NavBar />
      <div className="homepage-content">
        <div className="text-section">
          <h1>This is Your <span className="highlight">Assistant</span> for <br /> meetings and calls</h1>
          <p>Maximizes the productivity of online meetings with its AI-powered
             Noise Cancellation, Transcriptions and Diarization, Speaker Audio Clustering.
          </p>
        <div className='cta-btns'>
        <Link to="/sign-up" className="cta-button">Get it for free</Link>
          <Link to="/sign-up" style={{background: '#2c2c4d'}} className="cta-button">Try Now</Link>
        
        </div>
         
        </div>
        <div className="image-section">
          <SimulatedWaveform />
          {/* <img src={signalImage} alt="Product screenshot" /> */}
        </div>
      </div>
      <FeaturesSection />
      <TestimonialSection />
      <Footer />
      <button className="chat-button" onClick={toggleChatWindow}><BsFillChatTextFill /></button>
      {isChatOpen && <ChatWindow />}
    </div>
  );
}

export default HomePage;