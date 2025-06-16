import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AudioFeaturesPage.css'; // Import the CSS file for styling

function AudioFeaturesPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [featuresResult, setFeaturesResult] = useState(null);
  const [message, setMessage] = useState('');
  const [audioId, setAudioId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState(''); // Loading message state

  useEffect(() => {
    const accessToken = localStorage.getItem('token');
    console.log('Access Token on AudioFeaturesPage:', accessToken);
  }, []);

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleExtractFeatures = async () => {
    if (!selectedFile) {
      alert('Please upload an audio file first.');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      setLoading(true);
      setLoadingMessage('Uploading audio...'); // Set the initial loading message
  
      const accessToken = localStorage.getItem('token');
      console.log('Access Token before API call:', accessToken);
  
      // Upload the audio file
      await axios.post('http://localhost:5000/features', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${accessToken}`
        }
      });
  
      // After successful upload, update the loading message
      setLoadingMessage('Extracting features...'); // Change to extracting features
  
      // Call to extract features would typically go here, but it's included in the post request
      const response = await axios.post('http://localhost:5000/features', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${accessToken}`
        }
      });
  
      setFeaturesResult(response.data);
      setAudioId(response.data.audio_id);
      setMessage('Feature extraction successful!');
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setMessage('Session expired. Please log in again.');
      } else {
        setMessage('Error: ' + (error.response?.data?.error || error.message));
      }
    } finally {
      setLoading(false); // Stop loading
    }
  };
  

  // Function to download the features PDF
  const downloadFeaturesFile = async (audioId) => {
    try {
      const accessToken = localStorage.getItem('token');
      if (!accessToken) {
        setMessage('You need to log in first.');
        return;
      }

      const response = await axios.get(`http://localhost:5000/download_record/${audioId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'features.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove(); // Clean up the link
    } catch (error) {
      setMessage('Error downloading the features file.');
      console.error('Error downloading file:', error);
    }
  };

  const getFeatureImageUrl = (key) => {
    if (!featuresResult || !featuresResult.plot_paths || !featuresResult.plot_paths[key]) {
      return 'https://via.placeholder.com/150';
    }

    const path = featuresResult.plot_paths[key];
    return `http://localhost:5000/${path}`;
  };

  return (
    <div className="audio-features-page">
      <h1>Audio Features Extraction</h1>
      <p>Discover key audio insights with extracted features, including Bit Rate, Decibels, and Tempo, all at your fingertips. Visualize your data through informative graphs and easily download your comprehensive features report!</p>
      <div className="upload-section">
        <label htmlFor="audio-upload" className="upload-label">Upload Audio File</label>
        <input type="file" id="audio-upload" accept="audio/*" onChange={handleFileChange} />
      </div>

      <button onClick={handleExtractFeatures} className="extract-features-button" disabled={loading}>
        {loading ? 'Extracting...' : 'Extract Features'}
      </button>

      {loading && ( // Display loading message and circular loader when loading is true
        <div className="loading-container">
          <p>{loadingMessage}</p>
          <div className="circular-loader"></div>
        </div>
      )}

      {message && <p>{message}</p>}
      {featuresResult && (
        <div className="features-result">
          <h3>Extracted Features:</h3>
          <span>Audio ID: {featuresResult.audio_id}</span>
          <span>Bit Rate: {featuresResult.bitrate}</span>
          <span>Decibels: {featuresResult.decibels}</span>
          <span>File Size: {featuresResult.file_size}</span>
          <span>File Name: {featuresResult.filename}</span>
          <span>Tempo: {featuresResult?.tempo?.join(', ')}</span>
          <img src={getFeatureImageUrl('frequency_spectrum')} alt="Frequency Spectrum" />
          <img src={getFeatureImageUrl('harmonicity')} alt="Harmonicity" />
          <img src={getFeatureImageUrl('loudness')} alt="Loudness" />
          <img src={getFeatureImageUrl('silence_speech_ratio')} alt="Silence-Speech Ratio" />
          <img src={getFeatureImageUrl('waveform_with_peak')} alt="Waveform with Peak" />
          <img src={getFeatureImageUrl('waveform_with_sr')} alt="Waveform with SR" />
          <button className="download-button" onClick={() => downloadFeaturesFile(audioId)}>
            Download Features PDF
          </button>
        </div>
      )}
    </div>
  );
}

export default AudioFeaturesPage;
