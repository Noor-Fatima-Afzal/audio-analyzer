import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function useAuth() {
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const saveTokenAndRedirect = (token, successMessage = 'Sign-in successful!') => {
    // Remove any previous token and store the new token
    localStorage.removeItem('token');
    localStorage.setItem('token', token);

    // Set the success message and navigate after 2 seconds
    setMessage(successMessage + ' Redirecting to homepage...');
    setTimeout(() => {
      navigate('/'); // Redirect to homepage
    }, 2000);
  };

  const handleOAuthCallback = () => {
    // Check for OAuth token in URL
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');

    if (token) {
      saveTokenAndRedirect(token, 'OAuth sign-in successful! Access token saved.');
    }
  };

  const handleFormSubmit = async (loginData, loginUrl) => {
    try {
      const response = await fetch(loginUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
      });

      const data = await response.json();
      if (response.ok) {
        const { token } = data;
        saveTokenAndRedirect(token);
      } else {
        setMessage('Sign-in failed: ' + data.message);
      }
    } catch (error) {
      setMessage('Sign-in failed: ' + error.message);
    }
  };

  return {
    message,
    handleOAuthCallback,
    handleFormSubmit,
  };
}

export default useAuth;
