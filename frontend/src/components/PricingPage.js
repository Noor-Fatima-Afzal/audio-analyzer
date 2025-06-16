import React from 'react';
import './PricingPage.css'; // Importing the CSS file for styling

function PricingPage() {
  return (
    <div className="pricing-page">
      <h1>Pricing Plans</h1>
      <div className="pricing-list">
        <div className="pricing-card">
          <h2>Basic Plan</h2>
          <p>$10/month</p>
          <ul>
            <li>Feature 1</li>
            <li>Feature 2</li>
            <li>Feature 3</li>
          </ul>
          <button className="pricing-btn">Choose Plan</button>
        </div>
        <div className="pricing-card">
          <h2>Standard Plan</h2>
          <p>$20/month</p>
          <ul>
            <li>Feature 1</li>
            <li>Feature 2</li>
            <li>Feature 3</li>
            <li>Feature 4</li>
          </ul>
          <button className="pricing-btn">Choose Plan</button>
        </div>
        <div className="pricing-card">
          <h2>Premium Plan</h2>
          <p>$30/month</p>
          <ul>
            <li>Feature 1</li>
            <li>Feature 2</li>
            <li>Feature 3</li>
            <li>Feature 4</li>
            <li>Feature 5</li>
          </ul>
          <button className="pricing-btn">Choose Plan</button>
        </div>
      </div>
    </div>
  );
}

export default PricingPage;