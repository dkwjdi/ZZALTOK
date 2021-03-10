-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: jjal
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board` (
  `board_no` int NOT NULL AUTO_INCREMENT COMMENT 'board_no',
  `content_type` varchar(200) COLLATE utf8_unicode_ci NOT NULL COMMENT 'content_type',
  `content` longtext COLLATE utf8_unicode_ci NOT NULL COMMENT 'content',
  `nickname` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'nickname',
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'password',
  `ip` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT 'ip',
  `good` int NOT NULL DEFAULT '0' COMMENT 'good',
  `regdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`board_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='board';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_no` int NOT NULL AUTO_INCREMENT COMMENT 'comment_no',
  `board_no` int NOT NULL COMMENT 'board_no',
  `comment` longtext COLLATE utf8_unicode_ci NOT NULL COMMENT 'comment',
  `nickname` varchar(45) COLLATE utf8_unicode_ci NOT NULL COMMENT 'nickname',
  `password` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'password',
  `ip` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT 'ip',
  `regdate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_no`),
  KEY `FK_comment_board_no_board_board_no` (`board_no`),
  CONSTRAINT `FK_comment_board_no_board_board_no` FOREIGN KEY (`board_no`) REFERENCES `board` (`board_no`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='comment';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `most`
--

DROP TABLE IF EXISTS `most`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `most` (
  `most_no` int NOT NULL AUTO_INCREMENT COMMENT 'most_no',
  `most_count` int NOT NULL DEFAULT '0' COMMENT 'count',
  `most_name` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'name',
  `most_type` varchar(100) COLLATE utf8_unicode_ci NOT NULL COMMENT 'type',
  PRIMARY KEY (`most_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='most';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `most`
--

LOCK TABLES `most` WRITE;
/*!40000 ALTER TABLE `most` DISABLE KEYS */;
/*!40000 ALTER TABLE `most` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-09 14:39:53
