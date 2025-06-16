import React, { useState } from 'react';
import './NoiseCancellationPage.css'; // You can style this page similarly to others

function NoiseCancellationPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cancellationResult, setCancellationResult] = useState('');

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Mock function to handle Noise Cancellation
  const handleCancelNoise = () => {
    if (!selectedFile) {
      alert('Please upload an audio file first.');
      return;
    }

    // integrate with a Noise Cancellation API here
    // Mock Noise Cancellation response for demonstration
    setCancellationResult('Noise-canceled audio will appear here. (This is just a demo.)');
  };

  return (
    <div className="noise-cancellation-page">
      <h1>Noise Cancellation</h1>
      <p>Upload an audio file to eliminate background noise for clearer audio during your calls and meetings.</p>

      <div className="upload-section">
        <label htmlFor="audio-upload" className="upload-label">Upload Audio File</label>
        <input type="file" id="audio-upload" accept="audio/*" onChange={handleFileChange} />
      </div>

      <button onClick={handleCancelNoise} className="noise-cancellation-button">Cancel Noise</button>

      {cancellationResult && (
        <div className="noise-cancellation-result">
          <h3>Noise Cancellation Result:</h3>
          <p>{cancellationResult}</p>
        </div>
      )}
    </div>
  );
}

export default NoiseCancellationPage;
