import React from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import './NavBar.css'; // Importing the CSS file for styling

function NavBar() {

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">DataLabb</Link>
      </div>
      <ul className="navbar-links">
        <li><Link to="/products">Products</Link></li>
        <li><Link to="/use-cases">Use Cases</Link></li>
        <li><Link to="/pricing">Pricing</Link></li>
        <li><Link to="/blog">Blog</Link></li>
        <li><Link to="/how-it-works">How it works?</Link></li>
      </ul>
      <div className="navbar-buttons">
        <Link to="/login" className="navbar-signin">Sign in</Link>
        <Link to="/signup" className="navbar-btn purple-btn">Get it for free</Link>
        <Link to="/signup" className="navbar-btn dark-btn">Book a demo</Link>
        <Link to="/profile" className="navbar-btn light-btn">Profile</Link> 
      </div>
    </nav>
  );
}

export default NavBar;