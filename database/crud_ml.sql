-- phpMyAdmin SQL Dump
-- version 4.4.15.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 30, 2017 at 10:34 AM
-- Server version: 5.7.17-0ubuntu0.16.04.1
-- PHP Version: 7.0.13-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ml_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `username` varchar(50) UNIQUE NOT NULL,
    `password` varchar(100) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;


--
-- Table structure for table `historic`
--

CREATE TABLE IF NOT EXISTS `historic` (
    `id` int(5) PRIMARY KEY AUTO_INCREMENT,
    `ip` VARCHAR(50) NOT NULL,
    `country` VARCHAR(50) NOT NULL,
    `distance` DOUBLE NOT NULL,
    `count` INT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;


--
-- Table structure for table `log_tra`
--

CREATE TABLE IF NOT EXISTS `log_tra` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `create_by` INT NOT NULL,
    `create_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `min_distance` BOOLEAN,
    `max_distance` BOOLEAN,
    `prom_country` BOOLEAN,
    `country` VARCHAR(50),
    FOREIGN KEY (create_by) REFERENCES user (id)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;