-- phpMyAdmin SQL Dump
-- version 5.1.1deb4
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 15, 2021 at 11:07 PM
-- Server version: 8.0.26
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tradeapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `Balance`
--

CREATE TABLE `Balance` (
  `shortname` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `quantity` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Coin`
--

CREATE TABLE `Coin` (
  `shortname` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `fullname` varchar(50) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Coin`
--

INSERT INTO `Coin` (`shortname`, `fullname`) VALUES
('BNB', 'BINANCE COIN'),
('BTC', 'BITCOIN'),
('DOGE', 'DOGECOIN'),
('ETH', 'ETHEREUM');

-- --------------------------------------------------------

--
-- Table structure for table `Trades`
--

CREATE TABLE `Trades` (
  `shortname` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `orderType` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `quantity` double NOT NULL,
  `tradeTime` datetime DEFAULT NULL,
  `basecoin` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `virtualbalance`
--

CREATE TABLE `virtualbalance` (
  `shortname` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Balance` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `virtualtrade`
--

CREATE TABLE `virtualtrade` (
  `basecoin` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `quotecoin` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `ordertype` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `tradetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Balance`
--
ALTER TABLE `Balance`
  ADD KEY `shortname` (`shortname`);

--
-- Indexes for table `Coin`
--
ALTER TABLE `Coin`
  ADD PRIMARY KEY (`shortname`);

--
-- Indexes for table `Trades`
--
ALTER TABLE `Trades`
  ADD KEY `shortname` (`shortname`),
  ADD KEY `basecoin` (`basecoin`);

--
-- Indexes for table `virtualbalance`
--
ALTER TABLE `virtualbalance`
  ADD KEY `shortname` (`shortname`);

--
-- Indexes for table `virtualtrade`
--
ALTER TABLE `virtualtrade`
  ADD KEY `basecoin` (`basecoin`),
  ADD KEY `quotecoin` (`quotecoin`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Balance`
--
ALTER TABLE `Balance`
  ADD CONSTRAINT `Balance_ibfk_1` FOREIGN KEY (`shortname`) REFERENCES `Coin` (`shortname`);

--
-- Constraints for table `Trades`
--
ALTER TABLE `Trades`
  ADD CONSTRAINT `Trades_ibfk_1` FOREIGN KEY (`shortname`) REFERENCES `Coin` (`shortname`),
  ADD CONSTRAINT `Trades_ibfk_2` FOREIGN KEY (`basecoin`) REFERENCES `Coin` (`shortname`);

--
-- Constraints for table `virtualbalance`
--
ALTER TABLE `virtualbalance`
  ADD CONSTRAINT `virtualbalance_ibfk_1` FOREIGN KEY (`shortname`) REFERENCES `Coin` (`shortname`);

--
-- Constraints for table `virtualtrade`
--
ALTER TABLE `virtualtrade`
  ADD CONSTRAINT `virtualtrade_ibfk_1` FOREIGN KEY (`basecoin`) REFERENCES `Coin` (`shortname`),
  ADD CONSTRAINT `virtualtrade_ibfk_2` FOREIGN KEY (`quotecoin`) REFERENCES `Coin` (`shortname`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
