import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfilePage = () => {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState(null);

  const token = localStorage.getItem('token');  // Retrieve the token from local storage

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        if (!token) {
          throw new Error('No token found');
        }

        const response = await axios.get('http://localhost:5000/profile', {
          headers: {
            Authorization: `Bearer ${token}`,  // Send the token in the Authorization header
          },
        });
        setProfile(response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
        setError(error.response?.data?.error || error.message);
      }
    };

    fetchProfile();
  }, [token]);

  return (
    <div>
      {error && <p>Error: {error}</p>}
      {profile ? (
        <div>
          <h1>Profile</h1>
          <p>Username: {profile.username}</p>
          <p>Email: {profile.email}</p>
          <p>Role: {profile.role}</p>

          <h2>Uploaded Audios</h2>
          {profile.uploads && profile.uploads.length > 0 ? (
            <ul>
              {profile.uploads.map((upload) => (
                <li key={upload.audio_id}>
                  <p>Filename: {upload.filename}</p>
                  <p>Bitrate: {upload.bitrate} kbps</p>
                  <p>File Size: {upload.file_size} MB</p>
                  <p>Decibels: {upload.decibels} dB</p>
                  <p>Tempo: {upload.tempo} BPM</p>
                  <p>
                    <a href={`/${upload.loudness_plot_path}`} target="_blank" rel="noopener noreferrer">Loudness Plot</a>
                  </p>
                </li>
              ))}
            </ul>
          ) : (
            <p>No uploads available.</p>
          )}
        </div>
      ) : (
        <p>Loading profile...</p>
      )}
    </div>
  );
};

export default ProfilePage;
