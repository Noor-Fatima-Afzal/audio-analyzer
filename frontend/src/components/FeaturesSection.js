import React from 'react';
import './FeaturesSection.css'; // Import the CSS file for styling

function FeaturesSection() {
  const features = [
    {
      title: "Transcription",
      description: "Convert your audio and video meetings into text format quickly and accurately.",
      link: "/transcription"
    },
    {
      title: "Diarization",
      description: "Identify and separate different speakers in your meetings for better clarity.",
      link: "/diarization"
    },
    {
      title: "Meeting Notes",
      description: "Automatically generate meeting notes to keep track of discussions and decisions.",
      link: "/meeting-notes"
    },
    {
      title: "Noise Cancellation",
      description: "Eliminate background noise for clearer audio during your calls and meetings.",
      link: "/noise-cancellation"
    },
    {
      title: "Features of Audio",
      description: "Extract useful features from audio files for analysis and insights.",
      link: "/audio-features"
    },
    {
      title: "Speaker Clustering",
      description: "Get the voice of a particular speaker, speaking at different instances, in a single waveform.",
      link: "/speaker-clutering"
    }
  ];

  return (
    <div className="features-section">
      <h2>Our Features</h2>
      <div className="features-container">
        {features.map((feature, index) => (
          <div className="feature-card" key={index}>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
            <a href={feature.link} className="feature-button">Try {feature.title}</a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FeaturesSection;