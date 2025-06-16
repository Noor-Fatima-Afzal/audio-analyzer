# AudioAppAPI

**AudioAppAPI** is a web application that allows users to upload audio files, extract relevant audio features, perform speaker diarization, transcription, and interact with a chatbot for queries and text summarization. It is built using **Flask** for the backend and **React** for the frontend.

---

## Features

- **User Authentication**: Sign up, log in, and authenticate users via JWT tokens.
- **Audio File Processing**: Upload audio files, calculate features like bitrate, decibels, tempo, and generate visualizations (waveforms, frequency spectrum).
- **Speaker Diarization**: Perform speaker diarization on uploaded audio to identify different speakers.
- **Audio Transcription**: Transcribe audio into text.
- **LLM Chat Interface**: Users can interact with a chatbot powered by Groq API to process queries.
- **Text Summarization**: Summarize long texts using machine learning models.

---

## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Backend API Documentation](#backend-api-documentation)
  - [User Authentication](#user-authentication)
  - [Audio File Processing](#audio-file-processing)
  - [Speaker Diarization](#speaker-diarization)
  - [Transcription](#transcription)
  - [Chat Interface](#chat-interface)
  - [Summarization](#summarization)
- [Frontend](#frontend)
- [License](#license)

---

## Technologies Used

- **Backend**: 
  - Flask (Python)
  - Flask-JWT-Extended (JWT Authentication)
  - MySQL (Database)
  - Flask-CORS (Cross-Origin Resource Sharing)
  - Groq API (for chat)
  - Various Python libraries for audio analysis and feature extraction (e.g., `librosa`, `pydub`, etc.)
  
- **Frontend**: 
  - React.js (JavaScript)
  - Axios (for HTTP requests)
  - Material-UI (for styling)
  
---

## Installation Instructions

### Prerequisites

- Python 3.7+
- Node.js 14+
- MySQL Database

### Clone the Repository

```bash
git clone https://github.com/your-username/AudioAppAPI.git
cd AudioAppAPI
