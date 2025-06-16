import React from 'react';
import './BlogPage.css'; // Importing the CSS file for styling

function BlogPage() {
  return (
    <div className="blog-page">
      <h1>Our Blog</h1>
      <div className="blog-list">
        <div className="blog-card">
          <h2>Blog Post 1</h2>
          <p>Summary of Blog Post 1. This post discusses...</p>
          <button className="blog-btn">Read More</button>
        </div>
        <div className="blog-card">
          <h2>Blog Post 2</h2>
          <p>Summary of Blog Post 2. This post discusses...</p>
          <button className="blog-btn">Read More</button>
        </div>
        <div className="blog-card">
          <h2>Blog Post 3</h2>
          <p>Summary of Blog Post 3. This post discusses...</p>
          <button className="blog-btn">Read More</button>
        </div>
        <div className="blog-card">
          <h2>Blog Post 4</h2>
          <p>Summary of Blog Post 4. This post discusses...</p>
          <button className="blog-btn">Read More</button>
        </div>
      </div>
    </div>
  );
}

export default BlogPage;