-- MySQL dump 10.18  Distrib 10.3.27-MariaDB, for debian-linux-gnueabihf (armv8l)
--
-- Host: localhost    Database: elite
-- ------------------------------------------------------
-- Server version	10.3.27-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Market`
--

DROP TABLE IF EXISTS `Market`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Market` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idMarket` bigint(255) NOT NULL,
  `StationName` varchar(255) NOT NULL,
  `StationType` varchar(255) NOT NULL,
  `StationSystem` varchar(255) NOT NULL,
  `StationAllegiance` varchar(255) NOT NULL,
  `StationGovernement` varchar(255) NOT NULL,
  `debut` datetime NOT NULL DEFAULT current_timestamp(),
  `fin` datetime NOT NULL DEFAULT '9999-12-31 00:00:00',
  PRIMARY KEY (`id`),
  KEY `Market_I` (`idMarket`,`debut`,`fin`)
) ENGINE=InnoDB AUTO_INCREMENT=63652 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `lowtemperaturediamond`
--

DROP TABLE IF EXISTS `lowtemperaturediamond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lowtemperaturediamond` (
  `idlowtemperaturediamond` int(11) NOT NULL AUTO_INCREMENT,
  `idMarket` bigint(255) NOT NULL,
  `Prix` double NOT NULL,
  `Debut` datetime NOT NULL,
  `Fin` datetime NOT NULL DEFAULT '9999-12-31 00:00:00',
  `Demand` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`idlowtemperaturediamond`),
  KEY `LD_M` (`idMarket`,`Debut`,`Fin`)
) ENGINE=InnoDB AUTO_INCREMENT=59248 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `lowtemperaturediamond_market`
--

DROP TABLE IF EXISTS `lowtemperaturediamond_market`;
/*!50001 DROP VIEW IF EXISTS `lowtemperaturediamond_market`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `lowtemperaturediamond_market` (
  `id` tinyint NOT NULL,
  `idMarket` tinyint NOT NULL,
  `StationName` tinyint NOT NULL,
  `StationSystem` tinyint NOT NULL,
  `StationAllegiance` tinyint NOT NULL,
  `StationGovernement` tinyint NOT NULL,
  `Prix` tinyint NOT NULL,
  `Debut` tinyint NOT NULL,
  `Fin` tinyint NOT NULL,
  `Type` tinyint NOT NULL,
  `Demand` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `opal`
--

DROP TABLE IF EXISTS `opal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `opal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idMarket` bigint(255) NOT NULL,
  `Prix` double NOT NULL,
  `Debut` datetime NOT NULL,
  `Fin` datetime NOT NULL DEFAULT '9999-12-31 00:00:00',
  `Demand` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `opal_date` (`Debut`,`Fin`,`idMarket`)
) ENGINE=InnoDB AUTO_INCREMENT=33359 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `opal_market`
--

DROP TABLE IF EXISTS `opal_market`;
/*!50001 DROP VIEW IF EXISTS `opal_market`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `opal_market` (
  `id` tinyint NOT NULL,
  `idMarket` tinyint NOT NULL,
  `StationName` tinyint NOT NULL,
  `StationSystem` tinyint NOT NULL,
  `StationAllegiance` tinyint NOT NULL,
  `StationGovernement` tinyint NOT NULL,
  `Prix` tinyint NOT NULL,
  `Debut` tinyint NOT NULL,
  `Fin` tinyint NOT NULL,
  `Type` tinyint NOT NULL,
  `Demand` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `position_carrier`
--

DROP TABLE IF EXISTS `position_carrier`;
/*!50001 DROP VIEW IF EXISTS `position_carrier`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `position_carrier` (
  `id` tinyint NOT NULL,
  `idMarket` tinyint NOT NULL,
  `StationName` tinyint NOT NULL,
  `StationType` tinyint NOT NULL,
  `StationSystem` tinyint NOT NULL,
  `StationAllegiance` tinyint NOT NULL,
  `StationGovernement` tinyint NOT NULL,
  `debut` tinyint NOT NULL,
  `fin` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vrai_market`
--

DROP TABLE IF EXISTS `vrai_market`;
/*!50001 DROP VIEW IF EXISTS `vrai_market`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vrai_market` (
  `id` tinyint NOT NULL,
  `idMarket` tinyint NOT NULL,
  `StationName` tinyint NOT NULL,
  `StationType` tinyint NOT NULL,
  `StationSystem` tinyint NOT NULL,
  `StationAllegiance` tinyint NOT NULL,
  `StationGovernement` tinyint NOT NULL,
  `debut` tinyint NOT NULL,
  `fin` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `lowtemperaturediamond_market`
--

/*!50001 DROP TABLE IF EXISTS `lowtemperaturediamond_market`*/;
/*!50001 DROP VIEW IF EXISTS `lowtemperaturediamond_market`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`utilisateur`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `lowtemperaturediamond_market` AS select `lowtemperaturediamond`.`idlowtemperaturediamond` AS `id`,`lowtemperaturediamond`.`idMarket` AS `idMarket`,`vrai_market`.`StationName` AS `StationName`,`vrai_market`.`StationSystem` AS `StationSystem`,`vrai_market`.`StationAllegiance` AS `StationAllegiance`,`vrai_market`.`StationGovernement` AS `StationGovernement`,`lowtemperaturediamond`.`Prix` AS `Prix`,`lowtemperaturediamond`.`Debut` AS `Debut`,`lowtemperaturediamond`.`Fin` AS `Fin`,'Diamond' AS `Type`,`lowtemperaturediamond`.`Demand` AS `Demand` from (`lowtemperaturediamond` join `vrai_market` on(`lowtemperaturediamond`.`idMarket` = `vrai_market`.`idMarket` and `lowtemperaturediamond`.`Debut` >= `vrai_market`.`debut` and `lowtemperaturediamond`.`Fin` <= `vrai_market`.`fin`)) group by `lowtemperaturediamond`.`idlowtemperaturediamond` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `opal_market`
--

/*!50001 DROP TABLE IF EXISTS `opal_market`*/;
/*!50001 DROP VIEW IF EXISTS `opal_market`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`utilisateur`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `opal_market` AS select `opal`.`id` AS `id`,`opal`.`idMarket` AS `idMarket`,`vrai_market`.`StationName` AS `StationName`,`vrai_market`.`StationSystem` AS `StationSystem`,`vrai_market`.`StationAllegiance` AS `StationAllegiance`,`vrai_market`.`StationGovernement` AS `StationGovernement`,`opal`.`Prix` AS `Prix`,`opal`.`Debut` AS `Debut`,`opal`.`Fin` AS `Fin`,'Opal' AS `Type`,`opal`.`Demand` AS `Demand` from (`opal` join `vrai_market` on(`opal`.`idMarket` = `vrai_market`.`idMarket` and `opal`.`Debut` >= `vrai_market`.`debut` and `opal`.`Fin` <= `vrai_market`.`fin`)) group by `opal`.`id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `position_carrier`
--

/*!50001 DROP TABLE IF EXISTS `position_carrier`*/;
/*!50001 DROP VIEW IF EXISTS `position_carrier`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`utilisateur`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `position_carrier` AS select `Market`.`id` AS `id`,`Market`.`idMarket` AS `idMarket`,`Market`.`StationName` AS `StationName`,`Market`.`StationType` AS `StationType`,`Market`.`StationSystem` AS `StationSystem`,`Market`.`StationAllegiance` AS `StationAllegiance`,`Market`.`StationGovernement` AS `StationGovernement`,`Market`.`debut` AS `debut`,`Market`.`fin` AS `fin` from `Market` where `Market`.`StationType` = 'fleetcarrier' and `Market`.`fin` >= current_timestamp() */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vrai_market`
--

/*!50001 DROP TABLE IF EXISTS `vrai_market`*/;
/*!50001 DROP VIEW IF EXISTS `vrai_market`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`utilisateur`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vrai_market` AS select `Market`.`id` AS `id`,`Market`.`idMarket` AS `idMarket`,`Market`.`StationName` AS `StationName`,`Market`.`StationType` AS `StationType`,`Market`.`StationSystem` AS `StationSystem`,`Market`.`StationAllegiance` AS `StationAllegiance`,`Market`.`StationGovernement` AS `StationGovernement`,`Market`.`debut` AS `debut`,`Market`.`fin` AS `fin` from `Market` where `Market`.`StationType` not in ('fleetcarrier','megaship') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-27  6:55:59
