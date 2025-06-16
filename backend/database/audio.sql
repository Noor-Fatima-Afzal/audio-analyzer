-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 05, 2024 at 07:57 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `audio`
--

-- --------------------------------------------------------

--
-- Table structure for table `diarization`
--

CREATE TABLE `diarization` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `diarization_output_file` varchar(255) NOT NULL,
  `diarization_graph_output` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diarization`
--

INSERT INTO `diarization` (`id`, `user_id`, `filename`, `diarization_output_file`, `diarization_graph_output`) VALUES
(5, 1, '20240710123716_Given.wav', 'static\\Kokab_20240710123716_Given.wav_diarization_result.txt', 'static\\Kokab_20240710123716_Given.wav_diarization_graph.png'),
(7, 1, '20240711111825_audio.mp3', 'static\\Kokab_20240711111825_audio.mp3_diarization_result.txt', 'static\\Kokab_20240711111825_audio.mp3_diarization_graph.png'),
(8, 1, '20240731200050_Given.wav', 'static\\Kokab_20240731200050_Given.wav_diarization_result.txt', 'static\\Kokab_20240731200050_Given.wav_diarization_graph.png');

-- --------------------------------------------------------

--
-- Table structure for table `diarization_audio`
--

CREATE TABLE `diarization_audio` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `diarization_output_audio` text NOT NULL,
  `diarization_graph_output` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diarization_audio`
--

INSERT INTO `diarization_audio` (`id`, `user_id`, `filename`, `diarization_output_audio`, `diarization_graph_output`) VALUES
(3, 1, '20240828204146_audio.mp3', '{\"SPEAKER_02\": \"static/SpeakersAudios\\\\Kokab_20240828204146_audio.mp3_speaker_SPEAKER_02.wav\", \"SPEAKER_01\": \"static/SpeakersAudios\\\\Kokab_20240828204146_audio.mp3_speaker_SPEAKER_01.wav\", \"SPEAKER_03\": \"static/SpeakersAudios\\\\Kokab_20240828204146_audio.mp3_speaker_SPEAKER_03.wav\", \"SPEAKER_00\": \"static/SpeakersAudios\\\\Kokab_20240828204146_audio.mp3_speaker_SPEAKER_00.wav\"}', '\"static\\\\Kokab_20240828204146_audio.mp3_diarization_graph.png\"'),
(4, 1, '20240828204836_audio.mp3', '{\"SPEAKER_02\": \"static/SpeakersAudios\\\\Kokab_20240828204836_audio.mp3_speaker_SPEAKER_02.wav\", \"SPEAKER_01\": \"static/SpeakersAudios\\\\Kokab_20240828204836_audio.mp3_speaker_SPEAKER_01.wav\", \"SPEAKER_03\": \"static/SpeakersAudios\\\\Kokab_20240828204836_audio.mp3_speaker_SPEAKER_03.wav\", \"SPEAKER_00\": \"static/SpeakersAudios\\\\Kokab_20240828204836_audio.mp3_speaker_SPEAKER_00.wav\"}', '\"static\\\\Kokab_20240828204836_audio.mp3_diarization_graph.png\"'),
(5, 1, '20240828205858_audio.mp3', '{\"SPEAKER_03\": \"static/SpeakersAudios\\\\Kokab_20240828205858_audio.mp3_speaker_SPEAKER_03.wav\", \"SPEAKER_00\": \"static/SpeakersAudios\\\\Kokab_20240828205858_audio.mp3_speaker_SPEAKER_00.wav\", \"SPEAKER_02\": \"static/SpeakersAudios\\\\Kokab_20240828205858_audio.mp3_speaker_SPEAKER_02.wav\", \"SPEAKER_01\": \"static/SpeakersAudios\\\\Kokab_20240828205858_audio.mp3_speaker_SPEAKER_01.wav\"}', '\"static/SpeakersAudios/graphs\\\\Kokab_20240828205858_audio.mp3_diarization_graph.png\"');

-- --------------------------------------------------------

--
-- Table structure for table `model`
--

CREATE TABLE `model` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `audio_id` int(11) NOT NULL,
  `transcription_output_file` varchar(255) NOT NULL,
  `diarization_output_file` varchar(255) NOT NULL,
  `diarization_graph_output` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `profile`
--

CREATE TABLE `profile` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `pp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profile`
--

INSERT INTO `profile` (`id`, `username`, `email`, `password`, `gender`, `dob`, `country`, `phone`, `pp`) VALUES
(1, 'Hadia', 'Hadia@gmail.com', 'Hello', 'Female', '2006-07-14', 'Pakistan', '+923104660377', '/static/profile_pics/profile_pic_Hadia_20240817_212237.png');

-- --------------------------------------------------------

--
-- Table structure for table `transcription`
--

CREATE TABLE `transcription` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `transcription_output_file` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transcription`
--

INSERT INTO `transcription` (`id`, `user_id`, `filename`, `transcription_output_file`) VALUES
(11, 1, '20240710132301_Given.wav', 'static\\Kokab_20240710132301_Given.wav_transcription_result.txt'),
(12, 1, '20240731204103_audio.mp3', 'static\\Kokab_20240731204103_audio.mp3_transcription_result.txt');

-- --------------------------------------------------------

--
-- Table structure for table `uploads`
--

CREATE TABLE `uploads` (
  `audio_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `bitrate` int(11) NOT NULL,
  `frequency_plot_path` varchar(255) NOT NULL,
  `waveform_plot_path` varchar(255) NOT NULL,
  `silence_speech_ratio_plot_path` varchar(255) NOT NULL,
  `plot_path_decibels` varchar(255) NOT NULL,
  `plot_path_sr` varchar(255) NOT NULL,
  `harmonicity_plot_path` varchar(255) NOT NULL,
  `decibals` double NOT NULL,
  `file_size` double NOT NULL,
  `tempo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uploads`
--

INSERT INTO `uploads` (`audio_id`, `user_id`, `filename`, `bitrate`, `frequency_plot_path`, `waveform_plot_path`, `silence_speech_ratio_plot_path`, `plot_path_decibels`, `plot_path_sr`, `harmonicity_plot_path`, `decibals`, `file_size`, `tempo`) VALUES
(67, 1, '20240710025947_audio.mp3', 256000, 'static\\Kokab_20240710025947_audio.mp3_plot_path_sr.png', 'static\\Kokab_20240710025947_audio.mp3_waveform_with_peak.png', 'static\\Kokab_20240710025947_audio.mp3_silence_speech_ratio.png', 'static\\Kokab_20240710025947_audio.mp3_loudness_plot.png', 'static\\Kokab_20240710025947_audio.mp3_waveform_with_sampling_rate.png', 'static\\Kokab_20240710025947_audio.mp3_harmonicity.png', 81.28908924052512, 15.675335884094238, '[135.99917763]');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `pp` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `gender`, `dob`, `country`, `phone`, `pp`) VALUES
(1, 'Kokab', 'kokabnaveed2002@gmail.com', 'scrypt:32768:8:1$k64SmAcYv2HqBddY$3f95e0b0a9f74ca4f148a6fcd7460992a4efb8b1e239aacd7feeba72dc9af59201131baf34f120eead834a986415b794e2688a0e131d9543c0b44a0431fbe17a', 'None', '2004-07-09', 'None', 'None', '/static/profile_pics/profile_pic_Kokab_20240828_204952.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `diarization`
--
ALTER TABLE `diarization`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `diarization_audio`
--
ALTER TABLE `diarization_audio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `model`
--
ALTER TABLE `model`
  ADD PRIMARY KEY (`id`),
  ADD KEY `audio_id` (`audio_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transcription`
--
ALTER TABLE `transcription`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `uploads`
--
ALTER TABLE `uploads`
  ADD PRIMARY KEY (`audio_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `diarization`
--
ALTER TABLE `diarization`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `diarization_audio`
--
ALTER TABLE `diarization_audio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `model`
--
ALTER TABLE `model`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `profile`
--
ALTER TABLE `profile`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `transcription`
--
ALTER TABLE `transcription`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `uploads`
--
ALTER TABLE `uploads`
  MODIFY `audio_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=86;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `diarization`
--
ALTER TABLE `diarization`
  ADD CONSTRAINT `diarization_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `diarization_audio`
--
ALTER TABLE `diarization_audio`
  ADD CONSTRAINT `diarization_audio_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `model`
--
ALTER TABLE `model`
  ADD CONSTRAINT `model_ibfk_1` FOREIGN KEY (`audio_id`) REFERENCES `uploads` (`audio_id`),
  ADD CONSTRAINT `model_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `transcription`
--
ALTER TABLE `transcription`
  ADD CONSTRAINT `transcription_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `uploads`
--
ALTER TABLE `uploads`
  ADD CONSTRAINT `uploads_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
