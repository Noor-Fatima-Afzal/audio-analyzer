import React from 'react';
import './HowItWorksPage.css'; // Importing the CSS file for styling

function HowItWorksPage() {
  return (
    <div className="how-it-works-page">
      <h1>How It Works</h1>
      <div className="steps-list">
        <div className="step-card">
          <h2>Step 1: Sign Up</h2>
          <p>Create an account to get started with our services.</p>
        </div>
        <div className="step-card">
          <h2>Step 2: Choose a Plan</h2>
          <p>Select the plan that best fits your needs.</p>
        </div>
        <div className="step-card">
          <h2>Step 3: Start Using</h2>
          <p>Access all features and start maximizing your productivity.</p>
        </div>
      </div>
    </div>
  );
}

export default HowItWorksPage;