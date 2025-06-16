import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TranscriptionPage.css';

function TranscriptionPage() {
  const [file, setFile] = useState(null);
  const [transcription, setTranscription] = useState(null);
  const [summary, setSummary] = useState(null); // New state for summary
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [recordId, setRecordId] = useState(null);
  const [loading, setLoading] = useState(false); // New state for loading
  const [loadingSummary, setLoadingSummary] = useState(false); // New state for summary loading

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('You need to log in first');
    }
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null); // Clear any previous errors when a new file is selected
  };

  const handleTranscribe = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    if (!file.name.endsWith('.mp3') && !file.name.endsWith('.wav')) {
      setError('Unsupported file format. Only .mp3 and .wav are allowed.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true); // Set loading to true when transcription starts
      setMessage('Uploading audio...'); // Initial message

      // Use setTimeout to change the message after 3 seconds
      const timer = setTimeout(() => {
        setMessage('Performing transcription...');
      }, 3000);

      const token = localStorage.getItem('token'); // Get the token from local storage
      if (!token) {
        setError('You need to log in first');
        setLoading(false);
        return;
      }

      const response = await axios.post('http://localhost:5000/transcription', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}` // Set the Authorization header with JWT token
        }
      });

      clearTimeout(timer); // Clear the timer if the upload is successful

      // Set the transcription data from the response
      setTranscription(response.data.transcription_content);
      setRecordId(response.data.audio_id); // Get the audio ID for download
      setMessage('Transcription successful!'); // Success message
    } catch (error) {
      // Handle errors like invalid token or file upload issues
      setError(error.response ? error.response.data.error : 'Error uploading file');
    } finally {
      setLoading(false); // Set loading to false when transcription is done
    }
  };

  const summarizeTranscription = async (transcriptionText) => {
    setLoadingSummary(true); // Set loading to true when summarization starts
    setMessage('Generating summary...'); // Set message for summary generation
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('You need to log in first');
        return;
      }

      const response = await axios.post('http://localhost:5000/summarize', {
        text: transcriptionText
      }, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      });

      // Set the summary from the response
      setSummary(response.data.summary);
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error summarizing transcription');
    } finally {
      setLoadingSummary(false); // Set loading to false when summarization is done
    }
  };

  const downloadTranscriptFile = async (audioId) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('You need to log in first');
        return;
      }

      const response = await axios.get(`http://localhost:5000/download_transcription/${audioId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      downloadTxtFile(response.data);
    } catch (error) {
      setError(error.response ? error.response.data.error : 'Error downloading file');
    }
  };

  const downloadTxtFile = (content) => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'transcript.txt';
    document.body.appendChild(element);
    element.click();
  };

  return (
    <div className="transcription-container">
      <h1>Transcription</h1>
      <p>Capture every detail of your meetings with an AI-powered voice assistant. Enhance productivity and focus on what truly matters while the technology handles the transcription!</p>
      <input type="file" accept=".mp3, .wav" onChange={handleFileChange} />
      <button onClick={handleTranscribe} className="transcription-button">
        Upload and Transcribe
      </button>

      {loading && ( // Display loading message and circular loader when loading is true
        <div className="loading-container">
          <p>{message}</p>
          <div className="circular-loader"></div>
        </div>
      )}

      {error && <div className="error">Error: {error}</div>}
      {transcription && (
        <div className="transcription-result">
          <h3>Transcription Result:</h3>
          <pre>{transcription}</pre>
          <button className="transcription-button" onClick={() => downloadTranscriptFile(recordId)}>
            Download Transcription
          </button>
          <button className="transcription-button" onClick={() => summarizeTranscription(transcription)}>
            Summarize Transcription
          </button>

          {loadingSummary && (
            <div className="loading-container">
              <p>Generating summary, please wait...</p>
              <div className="loading-bar">
                <div className="loading-progress"></div>
              </div>
            </div>
          )}

          {/* Display summary here only after it has been generated */}
          {summary && (
            <div className="summary-result">
              <h4>Summary:</h4>
              <pre>{summary}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default TranscriptionPage;
