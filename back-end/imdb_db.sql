-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1
-- Χρόνος δημιουργίας: 30 Νοε 2023 στις 12:03:15
-- Έκδοση διακομιστή: 10.4.27-MariaDB
-- Έκδοση PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `imdb_db`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `aka`
--

CREATE TABLE `aka` (
  `Title_id` int(10) NOT NULL,
  `ordering` int(10) NOT NULL,
  `Title` varchar(500) NOT NULL,
  `Region` varchar(100) NOT NULL,
  `Language` varchar(100) NOT NULL,
  `Type` varchar(100) NOT NULL,
  `Attributes` varchar(100) NOT NULL,
  `isOriginalTitle` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `episodes`
--

CREATE TABLE `episodes` (
  `Title_id` int(10) NOT NULL,
  `Season_Number` int(10) NOT NULL,
  `Episode_Number` int(10) NOT NULL,
  `Parent_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `genre`
--

CREATE TABLE `genre` (
  `Genre_id` int(10) NOT NULL,
  `Genre_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `known_for_titles`
--

CREATE TABLE `known_for_titles` (
  `Title_id` int(10) NOT NULL,
  `Professional_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `production_company`
--

CREATE TABLE `production_company` (
  `Company_Id` int(10) NOT NULL,
  `Company_Name` varchar(100) NOT NULL,
  `Department` varchar(100) NOT NULL,
  `City` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Adress` int(10) NOT NULL,
  `Phone_Number` int(20) NOT NULL,
  `Manager_Name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `production_company_professionals`
--

CREATE TABLE `production_company_professionals` (
  `Professional_id` int(10) NOT NULL,
  `Company_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `production_company_titles`
--

CREATE TABLE `production_company_titles` (
  `Title_id` int(10) NOT NULL,
  `Company_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `professionals`
--

CREATE TABLE `professionals` (
  `Professional_id` int(10) NOT NULL,
  `Primary_Name` varchar(100) NOT NULL,
  `Birth_Year` int(10) NOT NULL,
  `Death_Year` int(10) NOT NULL,
  `Primary_Profession` varchar(500) NOT NULL,
  `img_url_asset` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `professionals_titles`
--

CREATE TABLE `professionals_titles` (
  `Title_id` int(10) NOT NULL,
  `Professional_id` int(10) NOT NULL,
  `Category` varchar(100) NOT NULL,
  `Job` varchar(100) NOT NULL,
  `Character` varchar(100) NOT NULL,
  `Column` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `ratings`
--

CREATE TABLE `ratings` (
  `Title_id` int(10) NOT NULL,
  `Average_Rating` double NOT NULL,
  `Likes` int(100) NOT NULL,
  `Number_of_Votes` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `titles`
--

CREATE TABLE `titles` (
  `Title_id` int(10) NOT NULL,
  `Type` varchar(100) NOT NULL,
  `Primary_Title` varchar(500) NOT NULL,
  `Original_Title` varchar(500) NOT NULL,
  `Is_Adult` int(10) NOT NULL,
  `Start_Year` int(10) NOT NULL,
  `End_Year` int(10) NOT NULL,
  `Minutes` int(10) NOT NULL,
  `img_url` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `titles_genre`
--

CREATE TABLE `titles_genre` (
  `Title_id` int(10) NOT NULL,
  `Genre_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `users`
--

CREATE TABLE `users` (
  `User_Id` int(10) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Birthdate` date NOT NULL,
  `Role` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `user_titlerating`
--

CREATE TABLE `user_titlerating` (
  `Title_id` int(10) NOT NULL,
  `User_Id` int(10) NOT NULL,
  `Rating` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Δείκτες `user_titlerating`
--
DELIMITER $$
CREATE TRIGGER `updateAverageRatings` AFTER INSERT ON `user_titlerating` FOR EACH ROW Begin
  UPDATE ratings
    SET average_rating = (
        SELECT AVG(rating)
        FROM user_titlerating
        WHERE title_id = NEW.title_id
    )
    WHERE title_id = NEW.title_id;
End
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `updateVotes` AFTER INSERT ON `user_titlerating` FOR EACH ROW BEGIN
    UPDATE ratings
    SET Number_of_Votes = Number_of_Votes + 1
    WHERE Title_id = NEW.Title_id; 
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `user_watched`
--

CREATE TABLE `user_watched` (
  `Title_id` int(10) NOT NULL,
  `User_Id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Δείκτες `user_watched`
--
DELIMITER $$
CREATE TRIGGER `updateWatchlist` AFTER INSERT ON `user_watched` FOR EACH ROW BEGIN
    DELETE FROM watchlist_titles
    WHERE title_id = NEW.title_id
      AND watchlist_id IN (
          SELECT watchlist_id
          FROM watchlist
          WHERE user_id = NEW.user_id
      );
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `watchlist`
--

CREATE TABLE `watchlist` (
  `Watchlist_id` int(10) NOT NULL,
  `User_id` int(10) NOT NULL,
  `Watchlist_Name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `watchlist_titles`
--

CREATE TABLE `watchlist_titles` (
  `Title_id` int(10) NOT NULL,
  `Watchlist_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `aka`
--
ALTER TABLE `aka`
  ADD KEY `aka_fk1` (`Title_id`);

--
-- Ευρετήρια για πίνακα `episodes`
--
ALTER TABLE `episodes`
  ADD KEY `episode_fk1` (`Title_id`);

--
-- Ευρετήρια για πίνακα `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`Genre_id`);

--
-- Ευρετήρια για πίνακα `known_for_titles`
--
ALTER TABLE `known_for_titles`
  ADD KEY `known_for_fk1` (`Title_id`),
  ADD KEY `known_for_fk2` (`Professional_id`);

--
-- Ευρετήρια για πίνακα `production_company`
--
ALTER TABLE `production_company`
  ADD PRIMARY KEY (`Company_Id`);

--
-- Ευρετήρια για πίνακα `production_company_professionals`
--
ALTER TABLE `production_company_professionals`
  ADD KEY `production_company_professionals_fk1` (`Professional_id`),
  ADD KEY `production_company_professionals_fk2` (`Company_id`);

--
-- Ευρετήρια για πίνακα `production_company_titles`
--
ALTER TABLE `production_company_titles`
  ADD KEY `production_company_titles_fk1` (`Title_id`),
  ADD KEY `production_company_titles_fk2` (`Company_id`);

--
-- Ευρετήρια για πίνακα `professionals`
--
ALTER TABLE `professionals`
  ADD PRIMARY KEY (`Professional_id`);

--
-- Ευρετήρια για πίνακα `professionals_titles`
--
ALTER TABLE `professionals_titles`
  ADD KEY `professionals_titles_fk1` (`Title_id`),
  ADD KEY `professionals_titles_fk2` (`Professional_id`);

--
-- Ευρετήρια για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD KEY `rating_fk1` (`Title_id`);

--
-- Ευρετήρια για πίνακα `titles`
--
ALTER TABLE `titles`
  ADD PRIMARY KEY (`Title_id`);

--
-- Ευρετήρια για πίνακα `titles_genre`
--
ALTER TABLE `titles_genre`
  ADD KEY `genre_fk1` (`Title_id`),
  ADD KEY `genre_fk2` (`Genre_id`);

--
-- Ευρετήρια για πίνακα `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_Id`);

--
-- Ευρετήρια για πίνακα `user_titlerating`
--
ALTER TABLE `user_titlerating`
  ADD KEY `user_rating_fk1` (`Title_id`),
  ADD KEY `user_rating_fk2` (`User_Id`);

--
-- Ευρετήρια για πίνακα `user_watched`
--
ALTER TABLE `user_watched`
  ADD KEY `user_watched_fk1` (`Title_id`),
  ADD KEY `user_watched_fk2` (`User_Id`);

--
-- Ευρετήρια για πίνακα `watchlist`
--
ALTER TABLE `watchlist`
  ADD PRIMARY KEY (`Watchlist_id`),
  ADD KEY `watchlist_fk1` (`User_id`);

--
-- Ευρετήρια για πίνακα `watchlist_titles`
--
ALTER TABLE `watchlist_titles`
  ADD KEY `watchlist_titles_fk1` (`Title_id`),
  ADD KEY `watchlist_titles_fk2` (`Watchlist_id`);

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `aka`
--
ALTER TABLE `aka`
  ADD CONSTRAINT `aka_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `episodes`
--
ALTER TABLE `episodes`
  ADD CONSTRAINT `episode_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`);

--
-- Περιορισμοί για πίνακα `known_for_titles`
--
ALTER TABLE `known_for_titles`
  ADD CONSTRAINT `known_for_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `known_for_fk2` FOREIGN KEY (`Professional_id`) REFERENCES `professionals` (`Professional_id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `production_company_professionals`
--
ALTER TABLE `production_company_professionals`
  ADD CONSTRAINT `production_company_professionals_fk1` FOREIGN KEY (`Professional_id`) REFERENCES `professionals` (`Professional_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `production_company_professionals_fk2` FOREIGN KEY (`Company_id`) REFERENCES `production_company` (`Company_Id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `production_company_titles`
--
ALTER TABLE `production_company_titles`
  ADD CONSTRAINT `production_company_titles_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `production_company_titles_fk2` FOREIGN KEY (`Company_id`) REFERENCES `production_company` (`Company_Id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `professionals_titles`
--
ALTER TABLE `professionals_titles`
  ADD CONSTRAINT `professionals_titles_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `professionals_titles_fk2` FOREIGN KEY (`Professional_id`) REFERENCES `professionals` (`Professional_id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `rating_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `titles_genre`
--
ALTER TABLE `titles_genre`
  ADD CONSTRAINT `genre_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `genre_fk2` FOREIGN KEY (`Genre_id`) REFERENCES `genre` (`Genre_id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `user_titlerating`
--
ALTER TABLE `user_titlerating`
  ADD CONSTRAINT `user_rating_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `user_rating_fk2` FOREIGN KEY (`User_Id`) REFERENCES `users` (`User_Id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `user_watched`
--
ALTER TABLE `user_watched`
  ADD CONSTRAINT `user_watched_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `user_watched_fk2` FOREIGN KEY (`User_Id`) REFERENCES `users` (`User_Id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `watchlist`
--
ALTER TABLE `watchlist`
  ADD CONSTRAINT `watchlist_fk1` FOREIGN KEY (`User_id`) REFERENCES `users` (`User_Id`) ON UPDATE CASCADE;

--
-- Περιορισμοί για πίνακα `watchlist_titles`
--
ALTER TABLE `watchlist_titles`
  ADD CONSTRAINT `watchlist_titles_fk1` FOREIGN KEY (`Title_id`) REFERENCES `titles` (`Title_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `watchlist_titles_fk2` FOREIGN KEY (`Watchlist_id`) REFERENCES `watchlist` (`Watchlist_id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
