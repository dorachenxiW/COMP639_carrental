-- MySQL dump 10.13  Distrib 8.0.31, for macos12 (x86_64)
--
-- Host: localhost    Database: carrental
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `car`
--

DROP TABLE IF EXISTS `car`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `car` (
  `carid` int NOT NULL AUTO_INCREMENT,
  `numberplate` varchar(100) DEFAULT NULL,
  `model` varchar(255) DEFAULT NULL,
  `seatingcapacity` int DEFAULT NULL,
  `year` int DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `rentalperday` decimal(8,2) DEFAULT NULL,
  PRIMARY KEY (`carid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `car`
--

LOCK TABLES `car` WRITE;
/*!40000 ALTER TABLE `car` DISABLE KEYS */;
INSERT INTO `car` VALUES (1,'ABC111','Toyota Prius',5,2021,'rent out',50.05),(2,'ABC222','Ford Focus',5,2023,'in garage',68.88),(3,'ABC333','Mazda CX-60',5,2022,'rent out',88.99),(8,'UIE234','Toyota Corolla',5,2019,'in garage',66.90),(9,'NXI730','Mitsubishi ASX ',5,2022,'in garage',89.99),(10,'NXD809','Hyundai Imax',8,2018,'in garage',120.00),(11,'XMU347','Toyota Hiace',12,2016,'in garage',118.00),(12,'UJN870','Toyota Yaris',5,2022,'rent out',58.00),(13,'SNX903','Mitsubishi Outlander',7,2022,'in garage',118.00),(14,'INE526','Toyota Hilux',5,2021,'in garage',119.99),(15,'POQ459','Kia Carnival',8,2018,'in garage',135.80),(16,'MXU204','Haval Jolion',5,2023,'in garage',78.90),(17,'MJS790','Toyota C-HR',5,2021,'in garage',89.00),(18,'SJE745','Hyundai i30',5,2023,'in garage',60.00),(19,'IXO243','Mazda 6',5,2021,'in garage',68.00),(20,'JPO601','Holden Commodore RS Wagon',5,2023,'in garage',108.00),(21,'BYE870','Suzuki Swift',5,2020,'rent out',58.88),(22,'BXY234','Hyundai Elantra',5,2022,'in garage',67.00),(23,'CX083','Toyota Camry',5,2023,'rent out',75.00),(24,'CBE385','Nissan X-Trail',5,2020,'rent out',80.00),(25,'BWL480','Toyota Prado',5,2019,'in garage',119.99);
/*!40000 ALTER TABLE `car` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `customerid` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `carid` int DEFAULT NULL,
  PRIMARY KEY (`customerid`),
  KEY `carid` (`carid`),
  KEY `userid` (`userid`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`carid`) REFERENCES `car` (`carid`),
  CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,1,'James','Woods','2087 Great South RD','09 767 523',NULL),(3,7,'John','Doe','187 Great South Rd, Auckland','021 765 3832',NULL),(4,8,'Mary','Black','89 Tims Drive, Christchurch','027 345 9876',NULL),(5,9,'Archie','Leader','89a West Street, New Plymouth','028 763 1567',NULL),(6,10,'Bethany ','Jackson','14 Otto Lane, Queenstown','09 765 8321',NULL);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `staffid` int NOT NULL AUTO_INCREMENT,
  `userid` int DEFAULT NULL,
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `carid` int DEFAULT NULL,
  PRIMARY KEY (`staffid`),
  KEY `carid` (`carid`),
  KEY `userid` (`userid`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`carid`) REFERENCES `car` (`carid`),
  CONSTRAINT `staff_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,2,'Michael','Boom','12 Helenslee Rd, Pokeno','021 783 562',NULL),(2,3,'Dora','Wang','10 Lippiatt Crescent, Pokeno','021 028 76516',NULL),(5,11,'Leanna','Michelle','1098 Great South Rd, Puni','028 673 1625',NULL),(6,12,'Jamiee','Vital','90 Hitchen Rd, Pokeno','023 874 6782',NULL);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'james','$2b$12$spYXqINXnW56c807PZbSxekB0T2crqjLgeGKrB.HlWGVvKZiXWUeS','james@carrental.com','customer'),(2,'michael','$2b$12$DiALQX4oC8bGaDB0rwRojuFcEAN29Qar.e0xA9lT7/CB9FBWH/0ve','michael@carrental.com','staff'),(3,'dora','$2b$12$KfjWfLIkjTcMZnHvZwH7u.PxYOxw.s/CM/Hzc2Kyw8BRhJjQ8Eos6','dora@carrental.com','admin'),(7,'john','$2b$12$yu8Eeaql.I3bxZUzbhQWsusuMqk4YbRWeiJeKkEKs12Gl6X/ixlNC','john@customer.com','customer'),(8,'mary','$2b$12$dbeDqAFgpbGOa//ER/u4m.ju./FDl.WjTMMW1wrxy1ZcW2BEPp3Gq','mary@customer.com','customer'),(9,'archie','$2b$12$SSn/MZrhwodfodX5xpAn2uYlbsNP6yNmk1AgFXClwIjFz9Feb6WKO','archie@customer.com','customer'),(10,'bethany','$2b$12$/6J.Y4qXDJSv/YnqPjnTg.uG8cmTzX3lWkrRtSP3c9eocz5P/5r9O','bethany@customer.com','customer'),(11,'leanna','$2b$12$lX9Ysncb3HKxSBf6c71qjOz4EcGsfDmxQOSgo.zc2bgkeGxHBAGMm','leanna@carrental.com','staff'),(12,'jamiee','$2b$12$uhCuOtVRKP1UZr1hdwwSKeiNB59/CQWfm9QuPINT7T2gLM8nuGr5K','jamiee@carrental.com','staff');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-09 10:57:37
