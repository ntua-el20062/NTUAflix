-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 10 Ιαν 2024 στις 08:49:53
-- Έκδοση διακομιστή: 10.4.27-MariaDB
-- Έκδοση PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS ntuaflix;
CREATE SCHEMA ntuaflix;
USE ntuaflix;



--
-- Βάση δεδομένων: `imdb_db`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `aka`
--

CREATE TABLE `akas` (
  `titleId` varchar(50) NOT NULL,
  `ordering` int(10) NOT NULL,
  `title` varchar(500) NOT NULL,
  `region` varchar(100) DEFAULT NULL,
  `language` varchar(100) DEFAULT NULL,
  `types` varchar(100) DEFAULT NULL,
  `attributes` varchar(100) DEFAULT NULL,
  `isOriginalTitle` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
-- Δομή πίνακα για τον πίνακα `crew`
--

CREATE TABLE `crew` (
  `tconst` varchar(50) NOT NULL,
  `directors` varchar(1000) DEFAULT NULL,
  `writers` varchar(10000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Δομή πίνακα για τον πίνακα `episodes`
--

CREATE TABLE `episode` (
  `tconst` varchar(50) NOT NULL,
  `parentTconst` varchar(50) NOT NULL,
  `seasonNumber` int(10) DEFAULT NULL,
  `episodeNumber` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
-- Δομή πίνακα για τον πίνακα `professionals`
--

CREATE TABLE `namebasics` (
  `nconst` varchar(50) NOT NULL,
  `primaryName` varchar(100) NOT NULL,
  `birthYear` int(10) DEFAULT NULL,
  `deathYear` int(10) DEFAULT NULL,
  `primaryProfession` varchar(500) NOT NULL,
  `knownForTitles` varchar(10000) DEFAULT NULL,
  `img_url_asset` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
--
-- Δομή πίνακα για τον πίνακα `professionals_titles`
--

CREATE TABLE `principals` (
  `tconst` varchar(50) NOT NULL,
  `ordering` int(10) DEFAULT NULL,
  `nconst` varchar(50) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `job` varchar(100) DEFAULT NULL,
  `characters` varchar(100) DEFAULT NULL,
  `img_url_asset` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Δομή πίνακα για τον πίνακα `ratings`
--

CREATE TABLE `ratings` (
  `tconst` varchar(50) NOT NULL,
  `averageRating` double NOT NULL,
  `numVotes` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Δομή πίνακα για τον πίνακα `titles`
--

CREATE TABLE `titlebasics` (
  `tconst` varchar(50) NOT NULL,
  `titleType` varchar(100) NOT NULL,
  `primaryTitle` varchar(500) NOT NULL,
  `originalTitle` varchar(500) NOT NULL,
  `isAdult` int(10) NOT NULL,
  `startYear` int(10) NOT NULL,
  `endYear` int(10) DEFAULT NULL,
  `runtimeMinutes` int(50) DEFAULT NULL,
  `genres` varchar(10000) DEFAULT NULL,
  `img_url_asset` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Ευρετήρια για πίνακα `aka`
--
ALTER TABLE `akas`
  ADD KEY `akas_fk1` (`titleId`),
  ADD KEY `title` (`title`),
  ADD KEY `ordering` (`ordering`),
  ADD KEY `isOriginalTitle` (`isOriginalTitle`),
  ADD PRIMARY KEY(`titleId`,`ordering`);

--
-- Ευρετήρια για πίνακα `crew`
--
ALTER TABLE `crew`
  ADD KEY `crew_fk1` (`tconst`),
  ADD PRIMARY KEY (`tconst`);

--
-- Ευρετήρια για πίνακα `episodes`
--
ALTER TABLE `episode`
  ADD KEY `episode_fk1` (`tconst`),
  ADD PRIMARY KEY (`tconst`);

--
-- Ευρετήρια για πίνακα `professionals`
--
ALTER TABLE `namebasics`
  ADD PRIMARY KEY (`nconst`),
  ADD KEY `namebasics_fk1` (`knownForTitles`(768));

--
-- Ευρετήρια για πίνακα `professionals_titles`
--
ALTER TABLE `principals`
  ADD KEY `principals_fk1` (`tconst`),
  ADD KEY (`ordering`),
  ADD PRIMARY KEY(`tconst`,`ordering`);

--
-- Ευρετήρια για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD KEY `ratings_fk1` (`tconst`),
  ADD PRIMARY KEY (`tconst`),
  ADD KEY `averageRating` (`averageRating`);

--
-- Ευρετήρια για πίνακα `titles`
--
ALTER TABLE `titlebasics`
  ADD PRIMARY KEY (`tconst`),
  ADD KEY `genres` (`genres`(768)),
  ADD KEY `originalTitle` (`originalTitle`),
  ADD KEY `primaryTitle` (`primaryTitle`);

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `aka`
--
ALTER TABLE `akas`
  ADD CONSTRAINT `akas_fk1` FOREIGN KEY (`titleId`) REFERENCES `titlebasics` (`tconst`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `crew`
--
ALTER TABLE `crew`
  ADD CONSTRAINT `crew_fk1` FOREIGN KEY (`tconst`) REFERENCES `titlebasics` (`tconst`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `episodes`
--
ALTER TABLE `episode`
  ADD CONSTRAINT `episode_fk1` FOREIGN KEY (`tconst`) REFERENCES `titlebasics` (`tconst`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `professionals_titles`
--
ALTER TABLE `principals`
  ADD CONSTRAINT `principals_fk1` FOREIGN KEY (`tconst`) REFERENCES `titlebasics` (`tconst`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_fk1` FOREIGN KEY (`tconst`) REFERENCES `titlebasics` (`tconst`) ON UPDATE CASCADE;






COMMIT;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
