import React, { useState } from 'react';
import './MeetingNotesPage.css';

function MeetingNotesPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [meetingNotes, setMeetingNotes] = useState('');

  // Handle file input change
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Mock function to handle Meeting Notes generation
  const handleGenerateNotes = () => {
    if (!selectedFile) {
      alert('Please upload a meeting audio file first.');
      return;
    }

    // You can integrate with a Meeting Notes API here
    // Mock Meeting Notes response for demonstration
    setMeetingNotes('Meeting notes will appear here. (This is just a demo.)');
  };

  return (
    <div className="meeting-notes-page">
      <h1>Meeting Notes Generator</h1>
      <p>Upload a meeting audio file to automatically generate notes for your discussion.</p>

      <div className="upload-section">
        <label htmlFor="audio-upload" className="upload-label">Upload Meeting Audio</label>
        <input type="file" id="audio-upload" accept="audio/*" onChange={handleFileChange} />
      </div>

      <button onClick={handleGenerateNotes} className="notes-button">Generate Meeting Notes</button>

      {meetingNotes && (
        <div className="meeting-notes-result">
          <h3>Generated Meeting Notes:</h3>
          <p>{meetingNotes}</p>
        </div>
      )}
    </div>
  );
}

export default MeetingNotesPage;
