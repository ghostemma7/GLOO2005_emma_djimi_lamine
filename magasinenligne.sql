-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: magasinenligne
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `idClient` int NOT NULL,
  `idUtilisateur` int NOT NULL,
  PRIMARY KEY (`idClient`),
  KEY `idUtilisateur_idx` (`idUtilisateur`),
  CONSTRAINT `idUtilisateur_C` FOREIGN KEY (`idUtilisateur`) REFERENCES `utilisateur` (`idUtilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commandes`
--

DROP TABLE IF EXISTS `commandes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `commandes` (
  `idCommandes` int NOT NULL,
  `Date_Commande` date NOT NULL,
  `CoutTotal` decimal(10,0) NOT NULL,
  `statut` varchar(30) NOT NULL,
  `idClient` int DEFAULT NULL,
  PRIMARY KEY (`idCommandes`),
  KEY `idClient_idx` (`idClient`),
  CONSTRAINT `idClient` FOREIGN KEY (`idClient`) REFERENCES `client` (`idClient`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commandes`
--

LOCK TABLES `commandes` WRITE;
/*!40000 ALTER TABLE `commandes` DISABLE KEYS */;
/*!40000 ALTER TABLE `commandes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluer`
--

DROP TABLE IF EXISTS `evaluer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluer` (
  `idCommentaire` int NOT NULL,
  `commentaire` text NOT NULL,
  `note` decimal(2,1) DEFAULT NULL,
  `dateNote` date DEFAULT NULL,
  `idProduits` int DEFAULT NULL,
  PRIMARY KEY (`idCommentaire`),
  KEY `idProduitsCom_idx` (`idProduits`),
  CONSTRAINT `idProduitsCom` FOREIGN KEY (`idProduits`) REFERENCES `produits` (`idProduits`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluer`
--

LOCK TABLES `evaluer` WRITE;
/*!40000 ALTER TABLE `evaluer` DISABLE KEYS */;
/*!40000 ALTER TABLE `evaluer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jouets`
--

DROP TABLE IF EXISTS `jouets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jouets` (
  `idJouets` int NOT NULL,
  `nomJouets` varchar(45) DEFAULT NULL,
  `idProduits` int DEFAULT NULL,
  PRIMARY KEY (`idJouets`),
  KEY `idProduits_J_idx` (`idProduits`),
  KEY `idx_jouet` (`idJouets`),
  CONSTRAINT `idProduits_J` FOREIGN KEY (`idProduits`) REFERENCES `produits` (`idProduits`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jouets`
--

LOCK TABLES `jouets` WRITE;
/*!40000 ALTER TABLE `jouets` DISABLE KEYS */;
/*!40000 ALTER TABLE `jouets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `livres`
--

DROP TABLE IF EXISTS `livres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `livres` (
  `idLivres` int NOT NULL,
  `nomLivre` varchar(45) NOT NULL,
  `idProduits` int DEFAULT NULL,
  PRIMARY KEY (`idLivres`),
  KEY `idProduits_idx` (`idProduits`),
  KEY `idx_livres` (`idLivres`),
  CONSTRAINT `idProduits` FOREIGN KEY (`idProduits`) REFERENCES `produits` (`idProduits`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `livres`
--

LOCK TABLES `livres` WRITE;
/*!40000 ALTER TABLE `livres` DISABLE KEYS */;
/*!40000 ALTER TABLE `livres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produits`
--

DROP TABLE IF EXISTS `produits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produits` (
  `idProduits` int NOT NULL,
  `nomProduits` varchar(100) NOT NULL,
  `prixProduit` decimal(10,0) NOT NULL,
  `description` varchar(45) NOT NULL,
  `typeProduits` enum('livres','jouets') NOT NULL,
  `idCommandes` int DEFAULT NULL,
  PRIMARY KEY (`idProduits`),
  KEY `idCommandes_idx` (`idCommandes`),
  CONSTRAINT `idCommandes` FOREIGN KEY (`idCommandes`) REFERENCES `commandes` (`idCommandes`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produits`
--

LOCK TABLES `produits` WRITE;
/*!40000 ALTER TABLE `produits` DISABLE KEYS */;
/*!40000 ALTER TABLE `produits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilisateur` (
  `idUtilisateur` int NOT NULL,
  `nomUtilisateur` char(45) DEFAULT NULL,
  `email` varchar(80) NOT NULL,
  `motPasse` varchar(45) NOT NULL,
  `dateInscription` date NOT NULL,
  `typeUtilisateur` enum('vendeur','clients') NOT NULL,
  PRIMARY KEY (`idUtilisateur`),
  KEY `idx_idUtilisateur` (`idUtilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilisateur`
--

LOCK TABLES `utilisateur` WRITE;
/*!40000 ALTER TABLE `utilisateur` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilisateur` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendeur`
--

DROP TABLE IF EXISTS `vendeur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendeur` (
  `noVendeur` int NOT NULL,
  `idUtilisateur` int DEFAULT NULL,
  KEY `idUtilisateur_idx` (`idUtilisateur`),
  CONSTRAINT `idUtilisateur_v` FOREIGN KEY (`idUtilisateur`) REFERENCES `utilisateur` (`idUtilisateur`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendeur`
--

LOCK TABLES `vendeur` WRITE;
/*!40000 ALTER TABLE `vendeur` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendeur` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-27 23:41:50
