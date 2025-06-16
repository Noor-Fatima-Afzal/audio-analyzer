import React from 'react';
import './Footer.css'; // Make sure to create this CSS file for styling
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-column">
          <h4>Products</h4>
          <ul>
            <li><a href="/ai-noise-cancellation">AI Noise Cancellation</a></li>
            <li><a href="/meeting-transcription">Meeting Transcription</a></li>
            <li><a href="/meeting-notes">AI Meeting Notes and Summary</a></li>
            <li><a href="/meeting-recording">Meeting Recording</a></li>
            <li><a href="/ai-accent">AI Accent Localization</a></li>
            <li><a href="/ai-interpreter">AI Live Interpreter</a></li>
            <li><a href="/ai-copilot">AI Agent Copilot</a></li>
            <li><a href="/speech-to-text">Speech-to-Text API</a></li>
            <li><a href="/call-recording">Call Recording API</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>Use Cases</h4>
          <ul>
            <li><a href="/call-center">Call Center (Enterprise)</a></li>
            <li><a href="/bpo">Call Center (BPO)</a></li>
            <li><a href="/professional-services">Professional Services</a></li>
            <li><a href="/sales-success">Sales and Success</a></li>
            <li><a href="/hybrid-work">Hybrid Work</a></li>
            <li><a href="/sdk-dev">SDK and Developers</a></li>
            <li><a href="/freelancers">Individuals and Freelancers</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>Company</h4>
          <ul>
            <li><a href="/about">About us</a></li>
            <li><a href="/careers">Careers</a></li>
            <li><a href="/brand">Brand guidelines</a></li>
            <li><a href="/demo">Demo</a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/videos">Video tutorials</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>Trust</h4>
          <ul>
            <li><a href="/security">Security</a></li>
            <li><a href="/terms">Terms of use</a></li>
            <li><a href="/privacy-policy">Privacy policy</a></li>
            <li><a href="/privacy-humans">Privacy for humans</a></li>
            <li><a href="/accessibility">Accessibility</a></li>
            <li><a href="/cookies">Cookie policy</a></li>
          </ul>
        </div>
        <div className="footer-column">
          <h4>Help & Connect</h4>
          <ul>
            <li><a href="/help-center">Help center</a></li>
            <li><a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a></li>
            <li><a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a></li>
            <li><a href="https://youtube.com" target="_blank" rel="noopener noreferrer">YouTube</a></li>
            <li><a href="https://x.com" target="_blank" rel="noopener noreferrer">X</a></li>
          </ul>
        </div>
      </div>

      <div className="footer-bottom">
        <p>© 2024 DataLabb, Inc. All rights reserved.</p>
        <p>2150 Example Ave, Penthouse 1300, City, State, Zip, Country</p>
        <div className="footer-buttons">
          <Link to="/sign-up" className="footer-btn demo-btn">Book a demo</Link>
          <Link to="/sign-up" className="footer-btn free-btn">Get it for free</Link>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
