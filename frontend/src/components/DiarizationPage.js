import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DiarizationPage.css';

function DiarizationPage() {
  const [file, setFile] = useState(null);
  const [diarization, setDiarization] = useState([]);
  const [graphImageUrl, setGraphImageUrl] = useState(null);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [recordId, setRecordId] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const token = localStorage.getItem('token');
  useEffect(() => {
    if (!token) {
      setError('You need to log in first');
    }
  }, [token]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleDiarize = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    // Log the file type
    console.log('Selected file type:', file.type);

    // Validate file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!['mp3', 'wav'].includes(fileExtension)) {
      setError('Unsupported file format. Only .mp3 and .wav are allowed.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      if (!token) {
        setError('You need to log in first');
        return;
      }

      setIsLoading(true); // Show loading message
      setMessage('Uploading audio...'); // Set initial loading message

      // Use setTimeout to change the message after 3 seconds
      const timer = setTimeout(() => {
        setMessage('Performing speaker diarization...');
      }, 10000);

      // Upload the audio file
      const response = await axios.post('http://localhost:5000/diarization', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      });

      clearTimeout(timer); // Clear the timer if the upload is successful

      console.log('Diarization response:', response.data);
      setDiarization(response.data.diarization_content);
      setRecordId(response.data.audio_id);
      setGraphImageUrl(response.data.diarization_graph_output.replace('\\', '/'));
      setMessage('Diarization successful!');
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error uploading file');
    } finally {
      setIsLoading(false); // Hide loading message
    }
  };

  const downloadDiarizationFile = async (audioId) => {
    try {
      if (!token) {
        setError('You need to log in first');
        return;
      }

      const response = await axios.get(`http://localhost:5000/download_diarization/${audioId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.data) {
        downloadTxtFile(response.data);
      } else {
        setError('No data found for download.');
      }
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error downloading file');
      console.error('Error downloading file:', error.response);
    }
  };

  const downloadTxtFile = (content) => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'application/pdf' });
    element.href = URL.createObjectURL(file);
    element.download = 'diarization.pdf';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element); // Clean up the element
  };

  const getImageUrl = () => {
    if (graphImageUrl) {
      console.log(graphImageUrl);
      const url = `http://localhost:5000/${graphImageUrl}`;
      return url;
    }
    // temp image url
    return 'https://via.placeholder.com/150';
  };

  return (
    <div className="diarization-container">
      <h1>Diarization</h1>
      <p>Enhance your meeting experience with AI-driven diarization that distinguishes between different speakers. Easily track conversations and gain clearer insights from your discussions!</p>
      <input type="file" accept=".mp3, .wav" onChange={handleFileChange} />
      <button onClick={handleDiarize} className="diarization-button">
        Upload and Diarize
      </button>

      {isLoading && ( // Display loading message and circular loader when isLoading is true
        <div className="loading-container">
          <p>{message}</p>
          <div className="circular-loader"></div>
        </div>
      )}

      {error && <div className="error">Error: {error}</div>}
      {diarization.length > 0 && (
        <div className="diarization-result">
          <h3>Diarization Result:</h3>
          <ul>
            {diarization.map((entry, index) => (
              <li key={index} style={{ color: entry.color }}>
                <strong>{entry.speaker}</strong> at {entry.time}: {entry.content}
              </li>
            ))}
          </ul>
          <img src={getImageUrl()} alt="Diarization" />
          <button className="download-button" onClick={() => downloadDiarizationFile(recordId)}>
            Download Diarization Text
          </button>
        </div>
      )}
    </div>
  );
}

export default DiarizationPage;
