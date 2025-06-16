import React from 'react';
import './ProductPage.css'; // Importing the CSS file for styling

function ProductPage() {
  return (
    <div className="product-page">
      <h1>Our Products</h1>
      <div className="product-list">
        <div className="product-card">
          <h2>Product 1</h2>
          <p>Description of Product 1. This product helps you with...</p>
          <button className="product-btn">Learn More</button>
        </div>
        <div className="product-card">
          <h2>Product 2</h2>
          <p>Description of Product 2. This product helps you with...</p>
          <button className="product-btn">Learn More</button>
        </div>
        <div className="product-card">
          <h2>Product 3</h2>
          <p>Description of Product 3. This product helps you with...</p>
          <button className="product-btn">Learn More</button>
        </div>
      </div>
    </div>
  );
}

export default ProductPage;
