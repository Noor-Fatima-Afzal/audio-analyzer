import React, { useEffect, useState } from 'react';
import useAuth from './useAuth';
import './SignInPage.css';

function SignInPage() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const { message, handleOAuthCallback, handleFormSubmit } = useAuth();

  useEffect(() => {
    // Check if there is an OAuth token in the URL
    handleOAuthCallback();
  }, [handleOAuthCallback]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleFormSubmit(formData, 'http://localhost:5000/login');
  };

  const handleGoogleSignIn = () => {
    window.location.href = 'http://127.0.0.1:5000/login_with_google';
  };

  const handleGitHubSignIn = () => {
    window.location.href = 'http://127.0.0.1:5000/login_with_github';
  };

  return (
    <div className="signin-page">
      <h1>Sign In</h1>
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

        <button type="submit" className="signin-button">
          Sign In
        </button>
      </form>
      {message && <p>{message}</p>}

      <div className="oauth-buttons">
        <button onClick={handleGoogleSignIn} className="google-signin-button">
          Sign In with Google
        </button>
        <button onClick={handleGitHubSignIn} className="github-signin-button">
          Sign In with GitHub
        </button>
      </div>
    </div>
  );
}

export default SignInPage;
