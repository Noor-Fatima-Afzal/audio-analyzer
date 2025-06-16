import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignUpPage.css';

function SignUpPage() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'user',
  });

  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const accessToken = params.get('access_token');

    console.log("Access Token from URL:", accessToken); // Log the access token

    if (accessToken) {
        localStorage.setItem('access_token', accessToken);
        setMessage('OAuth sign-in successful! Access token saved. Redirecting to homepage...');

        setTimeout(() => {
            navigate('/');
        }, 5000);
    } else {
        console.log("No access token found in URL."); // Log if no token is found
    }
}, [navigate]);


  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/signup', formData);
      const { access_token } = response.data;

      localStorage.setItem('access_token', access_token); // Store the token
      setMessage('Signup successful! Access token saved. Redirecting to homepage...');
      console.log('Signup access token:', access_token);

      setTimeout(() => {
        navigate('/'); // Redirect to homepage
      }, 2000);
    } catch (error) {
      setMessage('Signup failed: ' + (error.response?.data?.message || error.message));
    }
  };

  const handleGoogleSignUp = () => {
    window.location.href = 'http://127.0.0.1:5000/login_with_google';
  };

  const handleGitHubSignUp = () => {
    window.location.href = 'http://127.0.0.1:5000/login_with_github';
  };

  return (
    <div className="signup-page">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="role">Role</label>
          <select
            id="role"
            name="role"
            value={formData.role}
            onChange={handleChange}
            required
          >
            <option value="admin">Admin</option>
            <option value="user">User</option>
            <option value="guest">Guest</option>
          </select>
        </div>

        <button type="submit" className="signup-button">
          Sign Up
        </button>
      </form>
      {message && <p>{message}</p>}

      <div className="oauth-buttons">
        <button onClick={handleGoogleSignUp} className="google-signup-button">
          Sign Up with Google
        </button>
        <button onClick={handleGitHubSignUp} className="github-signup-button">
          Sign Up with GitHub
        </button>
      </div>
    </div>
  );
}

export default SignUpPage;
