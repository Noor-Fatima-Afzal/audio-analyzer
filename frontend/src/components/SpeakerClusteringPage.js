import React, { useState } from 'react';
import './SpeakerClusteringPage.css'; // Style similar to NoiseCancellationPage.css

function SpeakerClusteringPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [clusteringResult, setClusteringResult] = useState('');

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Mock function to handle Speaker Clustering
  const handleClusterSpeakers = () => {
    if (!selectedFile) {
      alert('Please upload an audio file first.');
      return;
    }

    // You can integrate with a Speaker Clustering API here
    // Mock Speaker Clustering response for demonstration
    setClusteringResult('Speaker clusters will appear here. (This is just a demo.)');
  };

  return (
    <div className="speaker-clustering-page">
      <h1>Speaker Clustering</h1>
      <p>Upload an audio file to identify and separate different speakers within the audio.</p>

      <div className="upload-section">
        <label htmlFor="audio-upload" className="upload-label">Upload Audio File</label>
        <input type="file" id="audio-upload" accept="audio/*" onChange={handleFileChange} />
      </div>

      <button onClick={handleClusterSpeakers} className="speaker-clustering-button">Cluster Speakers</button>

      {clusteringResult && (
        <div className="speaker-clustering-result">
          <h3>Clustering Result:</h3>
          <p>{clusteringResult}</p>
        </div>
      )}
    </div>
  );
}

export default SpeakerClusteringPage;
