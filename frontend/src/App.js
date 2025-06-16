import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import TranscriptionPage from './components/TranscriptionPage';
import DiarizationPage from './components/DiarizationPage';
import MeetingNotesPage from './components/MeetingNotesPage';
import NoiseCancellationPage from './components/NoiseCancellationPage'; 
import SignUpPage from './components/SignUpPage';
import SignInPage from './components/SignInPage';
import ProductPage from './components/ProductPage';
import UseCasesPage from './components/UseCasesPage';
import PricingPage from './components/PricingPage';
import BlogPage from './components/BlogPage';
import HowItWorksPage from './components/HowItWorksPage';
import AudioFeaturesPage from './components/AudioFeaturesPage'; 
import ProfilePage from './components/ProfilePage';
import SpeakerClusteringPage from './components/SpeakerClusteringPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/transcription" element={<TranscriptionPage />} />
        <Route path="/diarization" element={<DiarizationPage />} />
        <Route path="/meeting-notes" element={<MeetingNotesPage />} />
        <Route path="/noise-cancellation" element={<NoiseCancellationPage />} /> 
        <Route path="/signup" element={<SignUpPage />} /> 
        <Route path="/login" element={<SignInPage />} /> 
        <Route path="/products" element={<ProductPage />} />
        <Route path="/use-cases" element={<UseCasesPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/blog" element={<BlogPage />} />
        <Route path="/how-it-works" element={<HowItWorksPage />} />
        <Route path="/audio-features" element={<AudioFeaturesPage />} /> 
        <Route path="/profile" element={<ProfilePage />} />
        <Route path='/speaker-clutering' element={<SpeakerClusteringPage />} />
      </Routes>
    </Router>
  );
}

export default App;
