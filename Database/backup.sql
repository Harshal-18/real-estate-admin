-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: localhost    Database: real_estate_db
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `amenities`
--

DROP TABLE IF EXISTS `amenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `amenities` (
  `amenity_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category` varchar(20) NOT NULL COMMENT 'lifestyle, sports, natural, security, connectivity, wellness',
  `icon_url` varchar(500) DEFAULT NULL,
  `description` text,
  `is_rare` tinyint(1) DEFAULT '0' COMMENT 'for rare amenities',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`amenity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amenities`
--

LOCK TABLES `amenities` WRITE;
/*!40000 ALTER TABLE `amenities` DISABLE KEYS */;
INSERT INTO `amenities` VALUES (1,'Swimming Pool','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07'),(2,'Gymnasium','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07'),(3,'Club House','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07'),(4,'Children\'s Play Area','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07'),(5,'Indoor Games','sports',NULL,NULL,0,1,'2025-07-16 05:53:07'),(6,'Landscaped Gardens','natural',NULL,NULL,0,1,'2025-07-16 05:53:07'),(7,'24/7 Security','security','','',0,1,'2025-07-16 05:53:07'),(8,'Tennis Court','sports',NULL,NULL,1,1,'2025-07-16 05:53:07'),(9,'Yoga Deck','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07'),(10,'Multipurpose Hall','lifestyle',NULL,NULL,0,1,'2025-07-16 05:53:07');
/*!40000 ALTER TABLE `amenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `approvals`
--

DROP TABLE IF EXISTS `approvals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `approvals` (
  `approval_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `is_mandatory` tinyint(1) DEFAULT '1',
  `category` varchar(20) DEFAULT 'legal' COMMENT 'legal, environmental, fire_safety, structural, other',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`approval_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `approvals`
--

LOCK TABLES `approvals` WRITE;
/*!40000 ALTER TABLE `approvals` DISABLE KEYS */;
INSERT INTO `approvals` VALUES (2,'Fire','This is a fire safety approval',1,'Fire','2025-07-16 04:45:54');
/*!40000 ALTER TABLE `approvals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `balcony_details`
--

DROP TABLE IF EXISTS `balcony_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `balcony_details` (
  `balcony_id` int NOT NULL AUTO_INCREMENT,
  `unit_type_id` int NOT NULL,
  `balcony_name` varchar(100) DEFAULT NULL COMMENT 'Master Bedroom Balcony, Living Room Balcony, etc.',
  `balcony_sequence` int DEFAULT '1' COMMENT 'For multiple balconies',
  `balcony_length` decimal(8,2) NOT NULL COMMENT 'in meters',
  `balcony_width` decimal(8,2) NOT NULL COMMENT 'in meters',
  `balcony_area` decimal(8,2) NOT NULL COMMENT 'in sq ft',
  `connected_room` varchar(50) DEFAULT NULL COMMENT 'master_bedroom, living_room, dining_room, kitchen',
  `access_type` varchar(30) DEFAULT 'sliding_door' COMMENT 'sliding_door, french_door, open',
  `balcony_type` varchar(30) DEFAULT 'regular' COMMENT 'regular, utility, sit_out, deck',
  `has_provision_for_washing_machine` tinyint(1) DEFAULT '0',
  `has_provision_for_drying` tinyint(1) DEFAULT '1',
  `has_safety_grill` tinyint(1) DEFAULT '1',
  `facing_direction` varchar(20) DEFAULT NULL COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
  `view_description` text COMMENT 'garden view, road view, park view, etc.',
  `floor_level` varchar(20) DEFAULT NULL COMMENT 'ground, podium, tower, terrace',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`balcony_id`),
  KEY `unit_type_id` (`unit_type_id`),
  CONSTRAINT `balcony_details_ibfk_1` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `balcony_details`
--

LOCK TABLES `balcony_details` WRITE;
/*!40000 ALTER TABLE `balcony_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `balcony_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cities` (
  `city_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES (1,'Bengaluru','Karnataka','India',12.97160000,77.59460000,'2025-07-16 07:32:22'),(2,'Ahmedabad','Gujarat','India',23.02260000,72.57140000,'2025-07-16 07:33:37'),(3,'Surat','Gujrat','India',NULL,NULL,'2025-07-16 07:35:18');
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `developers`
--

DROP TABLE IF EXISTS `developers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `developers` (
  `developer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `established_year` int DEFAULT NULL,
  `description` text,
  `logo_url` varchar(500) DEFAULT NULL,
  `website_url` varchar(500) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `contact_phone` varchar(20) DEFAULT NULL,
  `address` text,
  `total_projects` int DEFAULT '0',
  `completed_projects` int DEFAULT '0',
  `ongoing_projects` int DEFAULT '0',
  `rating` decimal(3,2) DEFAULT '0.00',
  `total_reviews` int DEFAULT '0',
  `is_verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`developer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `developers`
--

LOCK TABLES `developers` WRITE;
/*!40000 ALTER TABLE `developers` DISABLE KEYS */;
INSERT INTO `developers` VALUES (1,'Lodha Group',1980,'Lodha Group is India\'s largest residential real estate developer by sales and construction area.',NULL,'https://www.lodhagroup.com','sales@lodha.com',NULL,NULL,2,0,1,0.00,0,1,'2025-07-16 05:53:07'),(2,'East Park Developers',1995,'East Park Developers is known for quality construction and timely delivery.',NULL,'https://www.eastpark.com','info@eastpark.com',NULL,NULL,0,0,0,0.00,0,1,'2025-07-16 05:53:07'),(3,'Brigade Group',1986,'Brigade Group is one of India\'s leading property developers with over three decades of expertise.',NULL,'https://www.brigadegroup.com','sales@brigadegroup.com',NULL,NULL,2,0,0,0.00,0,1,'2025-07-16 05:53:07');
/*!40000 ALTER TABLE `developers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `door_window_specs`
--

DROP TABLE IF EXISTS `door_window_specs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `door_window_specs` (
  `spec_id` int NOT NULL AUTO_INCREMENT,
  `unit_type_id` int NOT NULL,
  `item_type` varchar(20) NOT NULL COMMENT 'door, window',
  `location` varchar(100) NOT NULL COMMENT 'main_entrance, master_bedroom, kitchen, etc.',
  `width` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `thickness` decimal(5,2) DEFAULT NULL COMMENT 'in mm',
  `material` varchar(50) DEFAULT NULL COMMENT 'wood, steel, aluminum, upvc, glass',
  `finish` varchar(50) DEFAULT NULL COMMENT 'polished, painted, laminated, etc.',
  `brand` varchar(100) DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL COMMENT 'premium, standard, economy',
  `is_security_door` tinyint(1) DEFAULT '0',
  `has_grill` tinyint(1) DEFAULT '0',
  `opening_type` varchar(30) DEFAULT NULL COMMENT 'sliding, hinged, folding, casement',
  `lock_type` varchar(50) DEFAULT NULL COMMENT 'mortise, cylindrical, smart_lock',
  `handle_type` varchar(50) DEFAULT NULL,
  `handle_material` varchar(30) DEFAULT NULL,
  `glass_type` varchar(50) DEFAULT NULL COMMENT 'clear, tinted, frosted, laminated',
  `glass_thickness` decimal(4,2) DEFAULT NULL COMMENT 'in mm',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`spec_id`),
  KEY `unit_type_id` (`unit_type_id`),
  CONSTRAINT `door_window_specs_ibfk_1` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `door_window_specs`
--

LOCK TABLES `door_window_specs` WRITE;
/*!40000 ALTER TABLE `door_window_specs` DISABLE KEYS */;
/*!40000 ALTER TABLE `door_window_specs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `localities`
--

DROP TABLE IF EXISTS `localities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localities` (
  `locality_id` int NOT NULL AUTO_INCREMENT,
  `city_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `locality_type` varchar(20) DEFAULT 'locality' COMMENT 'locality, micro_market, suburb',
  `pincode` varchar(10) DEFAULT NULL,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`locality_id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `localities_ibfk_1` FOREIGN KEY (`city_id`) REFERENCES `cities` (`city_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localities`
--

LOCK TABLES `localities` WRITE;
/*!40000 ALTER TABLE `localities` DISABLE KEYS */;
INSERT INTO `localities` VALUES (1,1,'Whitefield','micro_market','560066',12.96980000,77.75000000,NULL,'2025-07-16 05:53:07'),(2,1,'Hennur','locality','560043',13.02730000,77.63320000,NULL,'2025-07-16 05:53:07'),(3,1,'Vittal Mallya Road','locality','560001',12.97200000,77.59530000,NULL,'2025-07-16 05:53:07'),(4,2,'Kankariya_lake','round-about lake','380008',23.02260000,72.57140000,'This is the very famous lake of the ahmedabad with high rush on weekends and also on weekdays as well','2025-07-16 04:15:25');
/*!40000 ALTER TABLE `localities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type` varchar(20) NOT NULL COMMENT 'price_change, new_project, similar_property, reminder, update, promotional',
  `title` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `related_project_id` int DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `is_sent` tinyint(1) DEFAULT '0',
  `delivery_method` varchar(20) DEFAULT 'in_app' COMMENT 'email, sms, push, in_app',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `read_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`notification_id`),
  KEY `user_id` (`user_id`),
  KEY `related_project_id` (`related_project_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`related_project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (2,1,'price_change','Price Change','the price of project id 1 has been changed',1,0,1,'SMS','2025-07-16 05:37:08',NULL);
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price_history`
--

DROP TABLE IF EXISTS `price_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `price_history` (
  `price_history_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int DEFAULT NULL,
  `unit_type_id` int DEFAULT NULL,
  `old_price` decimal(15,2) DEFAULT NULL,
  `new_price` decimal(15,2) DEFAULT NULL,
  `old_price_per_sqft` decimal(10,2) DEFAULT NULL,
  `new_price_per_sqft` decimal(10,2) DEFAULT NULL,
  `change_percentage` decimal(5,2) DEFAULT NULL,
  `change_reason` varchar(255) DEFAULT NULL,
  `effective_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`price_history_id`),
  KEY `project_id` (`project_id`),
  KEY `unit_type_id` (`unit_type_id`),
  CONSTRAINT `price_history_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `price_history_ibfk_2` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price_history`
--

LOCK TABLES `price_history` WRITE;
/*!40000 ALTER TABLE `price_history` DISABLE KEYS */;
INSERT INTO `price_history` VALUES (2,2,3,1.00,12.00,1.00,12.00,NULL,'',NULL,'2025-07-22 07:16:50');
/*!40000 ALTER TABLE `price_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_amenities`
--

DROP TABLE IF EXISTS `project_amenities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_amenities` (
  `project_id` int NOT NULL,
  `amenity_id` int NOT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  `description` text,
  `area_size` decimal(10,2) DEFAULT NULL COMMENT 'in sq ft',
  `capacity` int DEFAULT NULL COMMENT 'number of people/units it can accommodate',
  `operating_hours` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`,`amenity_id`),
  KEY `amenity_id` (`amenity_id`),
  CONSTRAINT `project_amenities_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `project_amenities_ibfk_2` FOREIGN KEY (`amenity_id`) REFERENCES `amenities` (`amenity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_amenities`
--

LOCK TABLES `project_amenities` WRITE;
/*!40000 ALTER TABLE `project_amenities` DISABLE KEYS */;
INSERT INTO `project_amenities` VALUES (1,1,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(1,2,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(1,3,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(1,4,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(1,6,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(1,7,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,1,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,2,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,3,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,4,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,5,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,7,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(2,9,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,1,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,2,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,3,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,6,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,7,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,8,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07'),(3,10,1,NULL,NULL,NULL,NULL,'2025-07-16 05:53:07');
/*!40000 ALTER TABLE `project_amenities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_approvals`
--

DROP TABLE IF EXISTS `project_approvals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_approvals` (
  `project_id` int NOT NULL,
  `approval_id` int NOT NULL,
  `status` varchar(20) DEFAULT 'pending' COMMENT 'pending, approved, rejected, expired',
  `approval_number` varchar(100) DEFAULT NULL,
  `approval_date` date DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `issuing_authority` varchar(255) DEFAULT NULL,
  `document_url` varchar(500) DEFAULT NULL,
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`,`approval_id`),
  KEY `approval_id` (`approval_id`),
  CONSTRAINT `project_approvals_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `project_approvals_ibfk_2` FOREIGN KEY (`approval_id`) REFERENCES `approvals` (`approval_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_approvals`
--

LOCK TABLES `project_approvals` WRITE;
/*!40000 ALTER TABLE `project_approvals` DISABLE KEYS */;
INSERT INTO `project_approvals` VALUES (1,2,'pending ','145',NULL,NULL,'Harshal','','Hi','2025-07-16 04:47:52');
/*!40000 ALTER TABLE `project_approvals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_documents`
--

DROP TABLE IF EXISTS `project_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_documents` (
  `document_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `document_type` varchar(20) NOT NULL COMMENT 'brochure, price_list, floor_plan, master_plan, legal_doc, approval, other',
  `title` varchar(255) NOT NULL,
  `description` text,
  `file_url` varchar(500) NOT NULL,
  `file_size` bigint DEFAULT NULL COMMENT 'in bytes',
  `file_type` varchar(50) DEFAULT NULL,
  `is_public` tinyint(1) DEFAULT '1',
  `download_count` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`document_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `project_documents_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_documents`
--

LOCK TABLES `project_documents` WRITE;
/*!40000 ALTER TABLE `project_documents` DISABLE KEYS */;
INSERT INTO `project_documents` VALUES (1,2,'floor_plan','This is the floor plan','This is the floor plan','',100,'PDF',1,100,'2025-07-16 04:54:05');
/*!40000 ALTER TABLE `project_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_media`
--

DROP TABLE IF EXISTS `project_media`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_media` (
  `media_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `media_type` varchar(20) NOT NULL COMMENT 'image, video, virtual_tour, floor_plan, master_plan',
  `media_url` varchar(500) NOT NULL,
  `thumbnail_url` varchar(500) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  `media_category` varchar(20) DEFAULT 'exterior' COMMENT 'exterior, interior, amenities, views, construction, location',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`media_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `project_media_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_media`
--

LOCK TABLES `project_media` WRITE;
/*!40000 ALTER TABLE `project_media` DISABLE KEYS */;
INSERT INTO `project_media` VALUES (9,1,'image','uploads/Lodha_Haven.webp','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F571-lodha-haven-choodasandra%2Fviews-3DRender-4.webp&w=3840&q=75','','','photo',1,'2025-07-23 01:17:42'),(11,2,'image','uploads/East_Park_Residences.webp','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F335-east-park-residences-sarjapur-road%2Fviews-2.jpg&w=3840&q=75','Main photo','','photo',1,'2025-07-23 02:48:54'),(12,3,'image','uploads/Brigade_Insignia.webp','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F369-brigade-insignia-yelahanka%2Fviews-2.png&w=3840&q=75','This is the main photo','','photo',1,'2025-07-23 02:56:28'),(13,1,'image','uploads/Master_plan_Lodha_Haven.png','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F571-lodha-haven-choodasandra%2FmasterPlan.png&w=2048&q=75','Master plan','','master_plan',1,'2025-07-23 04:32:50'),(14,2,'image','uploads/Master_plan_East_Park_Residences.png','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F335-east-park-residences-sarjapur-road%2FmasterPlan-5.png&w=2048&q=75','Master plan','','master_plan',1,'2025-07-23 07:29:01'),(15,3,'image','uploads/Master_plan_Brigade_Insignia.png','https://www.propsoch.com/_next/image?url=https%3A%2F%2Fd1zk2x7mtoyb2b.cloudfront.net%2FProjectImages%2F369-brigade-insignia-yelahanka%2FmasterPlan-17.png&w=2048&q=75','Master plan','','master_plan',1,'2025-07-23 07:37:24');
/*!40000 ALTER TABLE `project_media` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `developer_id` int NOT NULL,
  `locality_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `project_type` varchar(20) DEFAULT 'residential' COMMENT 'residential, commercial, mixed',
  `property_type` varchar(20) NOT NULL COMMENT 'apartment, villa, plot, office, retail',
  `status` varchar(30) NOT NULL COMMENT 'under_construction, ready_to_move, new_launch, completed',
  `total_land_area` decimal(10,2) DEFAULT NULL COMMENT 'in acres',
  `total_units` int DEFAULT NULL,
  `unit_density` decimal(8,2) DEFAULT NULL COMMENT 'units per acre',
  `open_area_percentage` decimal(5,2) DEFAULT NULL,
  `park_area` decimal(8,2) DEFAULT NULL COMMENT 'in acres',
  `clubhouse_area` decimal(10,2) DEFAULT NULL COMMENT 'in sq ft',
  `min_price` decimal(15,2) DEFAULT NULL,
  `max_price` decimal(15,2) DEFAULT NULL,
  `price_per_sqft` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT 'INR',
  `launch_date` date DEFAULT NULL,
  `possession_date` date DEFAULT NULL,
  `completion_date` date DEFAULT NULL,
  `address` text,
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `approach_road_width` decimal(8,2) DEFAULT NULL COMMENT 'in meters',
  `nearest_metro_distance` decimal(8,2) DEFAULT NULL COMMENT 'in km',
  `airport_distance` decimal(8,2) DEFAULT NULL COMMENT 'in km',
  `rera_number` varchar(100) DEFAULT NULL,
  `rera_website` varchar(500) DEFAULT NULL,
  `rera_status` varchar(20) DEFAULT 'approved' COMMENT 'approved, pending, expired',
  `description` text,
  `highlights` text,
  `master_plan_url` varchar(500) DEFAULT NULL,
  `brochure_url` varchar(500) DEFAULT NULL,
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_description` text,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`),
  KEY `developer_id` (`developer_id`),
  KEY `locality_id` (`locality_id`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`developer_id`) REFERENCES `developers` (`developer_id`),
  CONSTRAINT `projects_ibfk_2` FOREIGN KEY (`locality_id`) REFERENCES `localities` (`locality_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,1,1,'Lodha Haven','residential','apartment','under_construction',9.10,250,50.00,77.00,0.90,73.00,15000000.00,30000000.00,8500.00,'INR','2023-01-15','2026-12-31',NULL,'Choodasandra, Bengaluru',NULL,NULL,17.00,4.17,NULL,'','','approved','Lodha Haven offers premium 2, 3 & 4 BHK apartments with world-class amenities in Whitefield, Bangalore.','','Master_plan_Lodha_Haven.png',NULL,'','',1,'2025-07-16 05:53:07'),(2,2,2,'East Park Residences','residential','apartment','under_construction',4.20,180,NULL,NULL,NULL,NULL,18000000.00,35000000.00,9200.00,'INR','2023-03-01','2026-06-30',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'approved','East Park Residences presents luxurious 3 & 4 BHK apartments in Hennur, Bangalore with modern amenities.',NULL,NULL,NULL,NULL,NULL,1,'2025-07-16 05:53:07'),(3,3,3,'Brigade Insignia','residential','apartment','ready_to_move',3.80,160,10.00,70.00,20.00,19.00,25000000.00,50000000.00,12500.00,'INR','2020-06-01','2024-03-31',NULL,'',NULL,NULL,NULL,NULL,NULL,'','','approved','Brigade Insignia offers ultra-luxury 3 & 4 BHK apartments in the heart of Bangalore with premium amenities.','',NULL,NULL,'','',1,'2025-07-16 05:53:07');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_comparisons`
--

DROP TABLE IF EXISTS `property_comparisons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_comparisons` (
  `comparison_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `project_ids` text NOT NULL COMMENT 'JSON Array of project IDs',
  `comparison_parameters` text COMMENT 'JSON - Parameters used for comparison',
  `session_id` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comparison_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `property_comparisons_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_comparisons`
--

LOCK TABLES `property_comparisons` WRITE;
/*!40000 ALTER TABLE `property_comparisons` DISABLE KEYS */;
/*!40000 ALTER TABLE `property_comparisons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property_units`
--

DROP TABLE IF EXISTS `property_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property_units` (
  `unit_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `unit_type_id` int NOT NULL,
  `tower_id` int NOT NULL,
  `unit_number` varchar(50) NOT NULL,
  `floor_number` int NOT NULL,
  `unit_position` varchar(20) DEFAULT NULL COMMENT 'corner, middle, end',
  `wing` varchar(10) DEFAULT NULL COMMENT 'A, B, C, etc.',
  `carpet_area` decimal(10,2) DEFAULT NULL,
  `built_up_area` decimal(10,2) DEFAULT NULL,
  `super_area` decimal(10,2) DEFAULT NULL,
  `has_corner_unit` tinyint(1) DEFAULT '0',
  `has_extra_balcony` tinyint(1) DEFAULT '0',
  `has_servant_quarter` tinyint(1) DEFAULT '0',
  `unit_price` decimal(15,2) DEFAULT NULL,
  `price_per_sqft` decimal(10,2) DEFAULT NULL,
  `maintenance_charge` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'available' COMMENT 'available, sold, blocked, reserved',
  `possession_date` date DEFAULT NULL,
  `premium_percentage` decimal(5,2) DEFAULT '0.00',
  `discount_percentage` decimal(5,2) DEFAULT '0.00',
  `actual_facing_direction` varchar(20) DEFAULT NULL,
  `view_description` text COMMENT 'garden view, road view, etc.',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `block_number` varchar(50) DEFAULT NULL,
  `booking_status` varchar(50) DEFAULT NULL,
  `possession_status` varchar(50) DEFAULT NULL,
  `base_price` decimal(15,2) DEFAULT NULL,
  `premium_charges` decimal(15,2) DEFAULT NULL,
  `other_charges` decimal(15,2) DEFAULT NULL,
  `total_price` decimal(15,2) DEFAULT NULL,
  `facing_direction` varchar(50) DEFAULT NULL,
  `view_type` varchar(50) DEFAULT NULL,
  `corner_unit` tinyint(1) DEFAULT '0',
  `has_private_terrace` tinyint(1) DEFAULT '0',
  `has_private_garden` tinyint(1) DEFAULT '0',
  `is_modified` tinyint(1) DEFAULT '0',
  `modifications` text,
  PRIMARY KEY (`unit_id`),
  KEY `project_id` (`project_id`),
  KEY `unit_type_id` (`unit_type_id`),
  KEY `tower_id` (`tower_id`),
  CONSTRAINT `property_units_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `property_units_ibfk_2` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`),
  CONSTRAINT `property_units_ibfk_3` FOREIGN KEY (`tower_id`) REFERENCES `towers` (`tower_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property_units`
--

LOCK TABLES `property_units` WRITE;
/*!40000 ALTER TABLE `property_units` DISABLE KEYS */;
INSERT INTO `property_units` VALUES (1,1,1,1,'A-1201',12,NULL,NULL,NULL,NULL,NULL,0,0,0,15500000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(2,1,2,2,'B-1502',15,NULL,NULL,NULL,NULL,NULL,0,0,0,22500000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(3,1,3,3,'C-1801',18,NULL,NULL,NULL,NULL,NULL,0,0,0,31000000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(4,2,4,4,'EW-1001',10,NULL,NULL,NULL,NULL,NULL,0,0,0,18500000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(5,2,5,5,'WW-1102',11,NULL,NULL,NULL,NULL,NULL,0,0,0,25500000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(6,2,6,6,'CT-1401',14,NULL,NULL,NULL,NULL,NULL,0,0,0,35500000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(7,3,7,7,'T1-2001',20,NULL,NULL,NULL,NULL,NULL,0,0,0,26000000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(8,3,8,8,'T2-2202',22,NULL,NULL,NULL,NULL,NULL,0,0,0,36000000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL),(9,3,9,9,'T3-2001',20,NULL,NULL,NULL,NULL,NULL,0,0,0,51000000.00,NULL,NULL,'available',NULL,0.00,0.00,NULL,NULL,1,'2025-07-16 05:53:07',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,0,NULL);
/*!40000 ALTER TABLE `property_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int DEFAULT NULL,
  `developer_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `review_text` text,
  `pros` text,
  `cons` text,
  `construction_quality_rating` int DEFAULT NULL,
  `amenities_rating` int DEFAULT NULL,
  `location_rating` int DEFAULT NULL,
  `value_for_money_rating` int DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  KEY `project_id` (`project_id`),
  KEY `developer_id` (`developer_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`developer_id`) REFERENCES `developers` (`developer_id`),
  CONSTRAINT `reviews_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `reviews_chk_1` CHECK (((`rating` >= 1) and (`rating` <= 5))),
  CONSTRAINT `reviews_chk_2` CHECK (((`construction_quality_rating` >= 1) and (`construction_quality_rating` <= 5))),
  CONSTRAINT `reviews_chk_3` CHECK (((`amenities_rating` >= 1) and (`amenities_rating` <= 5))),
  CONSTRAINT `reviews_chk_4` CHECK (((`location_rating` >= 1) and (`location_rating` <= 5))),
  CONSTRAINT `reviews_chk_5` CHECK (((`value_for_money_rating` >= 1) and (`value_for_money_rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_logs`
--

DROP TABLE IF EXISTS `search_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_logs` (
  `search_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `search_query` varchar(500) DEFAULT NULL,
  `filters_applied` text COMMENT 'JSON format',
  `results_count` int DEFAULT NULL,
  `clicked_project_id` int DEFAULT NULL,
  `search_timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `session_id` varchar(255) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`search_id`),
  KEY `user_id` (`user_id`),
  KEY `clicked_project_id` (`clicked_project_id`),
  CONSTRAINT `search_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `search_logs_ibfk_2` FOREIGN KEY (`clicked_project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_logs`
--

LOCK TABLES `search_logs` WRITE;
/*!40000 ALTER TABLE `search_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `search_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `towers`
--

DROP TABLE IF EXISTS `towers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `towers` (
  `tower_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `tower_name` varchar(100) NOT NULL,
  `tower_number` varchar(50) DEFAULT NULL,
  `total_floors` int NOT NULL,
  `units_per_floor` int DEFAULT '0',
  `total_units` int DEFAULT '0',
  `tower_type` varchar(20) DEFAULT 'residential' COMMENT 'residential, commercial, mixed',
  `construction_status` varchar(30) DEFAULT 'under_construction' COMMENT 'under_construction, completed, ready_to_move',
  `possession_date` date DEFAULT NULL,
  `height_meters` decimal(8,2) DEFAULT NULL,
  `elevator_count` int DEFAULT '0',
  `has_power_backup` tinyint(1) DEFAULT '1',
  `has_water_backup` tinyint(1) DEFAULT '1',
  `has_fire_safety` tinyint(1) DEFAULT '1',
  `latitude` decimal(10,8) DEFAULT NULL,
  `longitude` decimal(11,8) DEFAULT NULL,
  `facing_direction` varchar(20) DEFAULT NULL COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`tower_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `towers_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `towers`
--

LOCK TABLES `towers` WRITE;
/*!40000 ALTER TABLE `towers` DISABLE KEYS */;
INSERT INTO `towers` VALUES (1,1,'Haven A',NULL,20,4,80,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(2,1,'Haven B',NULL,20,4,80,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(3,1,'Haven C',NULL,22,4,88,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(4,2,'East Wing',NULL,15,4,60,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(5,2,'West Wing',NULL,15,4,60,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(6,2,'Central Tower',NULL,15,4,60,'residential','under_construction',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(7,3,'Insignia Tower 1',NULL,25,2,50,'residential','ready_to_move',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(8,3,'Insignia Tower 2',NULL,25,2,50,'residential','ready_to_move',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13'),(9,3,'Insignia Tower 3',NULL,20,3,60,'residential','ready_to_move',NULL,NULL,0,1,1,1,NULL,NULL,NULL,1,'2025-07-16 12:11:13');
/*!40000 ALTER TABLE `towers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit_room_details`
--

DROP TABLE IF EXISTS `unit_room_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit_room_details` (
  `room_detail_id` int NOT NULL AUTO_INCREMENT,
  `unit_type_id` int NOT NULL,
  `room_type` varchar(50) NOT NULL COMMENT 'master_bedroom, child_bedroom, guest_bedroom, living_room, dining_room, kitchen, bathroom, balcony, study_room, utility_room, store_room, pooja_room, foyer, passage',
  `room_name` varchar(100) DEFAULT NULL COMMENT 'Master Bedroom, Child Bedroom 1, Living Room, etc.',
  `room_sequence` int DEFAULT '1' COMMENT 'For multiple rooms of same type',
  `room_length` decimal(8,2) NOT NULL COMMENT 'in meters',
  `room_width` decimal(8,2) NOT NULL COMMENT 'in meters',
  `room_area` decimal(8,2) NOT NULL COMMENT 'in sq ft',
  `room_shape` varchar(30) DEFAULT 'rectangular' COMMENT 'rectangular, square, l_shaped, irregular',
  `has_attached_bathroom` tinyint(1) DEFAULT '0',
  `has_balcony_access` tinyint(1) DEFAULT '0',
  `has_wardrobe` tinyint(1) DEFAULT '0',
  `wardrobe_type` varchar(50) DEFAULT NULL COMMENT 'built-in, walk-in, modular',
  `wardrobe_area` decimal(6,2) DEFAULT NULL COMMENT 'in sq ft',
  `has_window` tinyint(1) DEFAULT '1',
  `window_count` int DEFAULT '1',
  `window_total_area` decimal(6,2) DEFAULT NULL COMMENT 'in sq ft',
  `natural_light_rating` varchar(10) DEFAULT 'good' COMMENT 'excellent, good, average, poor',
  `ventilation_rating` varchar(10) DEFAULT 'good' COMMENT 'excellent, good, average, poor',
  `door_count` int DEFAULT '1',
  `door_type` varchar(50) DEFAULT NULL COMMENT 'single, double, sliding, folding',
  `door_material` varchar(50) DEFAULT NULL COMMENT 'wood, steel, glass, composite',
  `door_width` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `door_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `window_type` varchar(50) DEFAULT NULL COMMENT 'sliding, casement, french, bay, fixed',
  `window_material` varchar(50) DEFAULT NULL COMMENT 'aluminum, upvc, wooden, steel',
  `window_width` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `window_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `electrical_points` int DEFAULT '0',
  `fan_points` int DEFAULT '0',
  `ac_points` int DEFAULT '0',
  `light_points` int DEFAULT '0',
  `flooring_type` varchar(50) DEFAULT NULL COMMENT 'marble, vitrified_tiles, ceramic, wooden, granite',
  `flooring_brand` varchar(100) DEFAULT NULL,
  `ceiling_type` varchar(50) DEFAULT NULL COMMENT 'pop, gypsum, concrete, wooden',
  `ceiling_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `has_geyser_provision` tinyint(1) DEFAULT '0',
  `has_exhaust_fan` tinyint(1) DEFAULT '0',
  `has_chimney_provision` tinyint(1) DEFAULT '0',
  `privacy_level` varchar(20) DEFAULT 'private' COMMENT 'private, semi_private, open',
  `position_in_unit` varchar(30) DEFAULT NULL COMMENT 'front, back, side, central, corner',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`room_detail_id`),
  KEY `unit_type_id` (`unit_type_id`),
  CONSTRAINT `unit_room_details_ibfk_1` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit_room_details`
--

LOCK TABLES `unit_room_details` WRITE;
/*!40000 ALTER TABLE `unit_room_details` DISABLE KEYS */;
INSERT INTO `unit_room_details` VALUES (1,9,'child_bedroom','child 1',1,1.00,1.00,1.00,'rectangular',1,1,1,'walk-in',1.00,1,1,1.00,'good','good',2,'single','wood',1.00,1.00,'s','glass',1.00,1.00,8,1,1,12,'marbel','a','pop',1.00,1,1,0,'private','back','2025-07-16 05:43:33');
/*!40000 ALTER TABLE `unit_room_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit_types`
--

DROP TABLE IF EXISTS `unit_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit_types` (
  `unit_type_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `type_name` varchar(100) NOT NULL COMMENT 'e.g., 3BHK, 4BHK+Maid, 1BHK+Study',
  `bedrooms` int NOT NULL,
  `bathrooms` int NOT NULL,
  `master_bedrooms` int DEFAULT '0',
  `child_bedrooms` int DEFAULT '0',
  `guest_bedrooms` int DEFAULT '0',
  `study_rooms` int DEFAULT '0',
  `living_rooms` int DEFAULT '1',
  `dining_rooms` int DEFAULT '0',
  `kitchens` int DEFAULT '1',
  `utility_rooms` int DEFAULT '0',
  `store_rooms` int DEFAULT '0',
  `pooja_rooms` int DEFAULT '0',
  `has_maid_room` tinyint(1) DEFAULT '0',
  `maid_room_area` decimal(8,2) DEFAULT NULL COMMENT 'in sq ft',
  `has_maid_bathroom` tinyint(1) DEFAULT '0',
  `has_balcony` tinyint(1) DEFAULT '1',
  `balcony_count` int DEFAULT '0',
  `total_balcony_area` decimal(8,2) DEFAULT NULL COMMENT 'in sq ft',
  `has_terrace` tinyint(1) DEFAULT '0',
  `terrace_area` decimal(8,2) DEFAULT NULL COMMENT 'in sq ft',
  `has_private_garden` tinyint(1) DEFAULT '0',
  `private_garden_area` decimal(8,2) DEFAULT NULL COMMENT 'in sq ft',
  `carpet_area` decimal(10,2) DEFAULT NULL COMMENT 'in sq ft',
  `built_up_area` decimal(10,2) DEFAULT NULL COMMENT 'in sq ft',
  `super_area` decimal(10,2) DEFAULT NULL COMMENT 'in sq ft',
  `carpet_ratio` decimal(5,2) DEFAULT NULL COMMENT 'carpet area percentage',
  `base_price` decimal(15,2) DEFAULT NULL,
  `price_per_sqft` decimal(10,2) DEFAULT NULL,
  `floor_plan_url` varchar(500) DEFAULT NULL,
  `floor_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `ceiling_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `facing_direction` varchar(20) DEFAULT NULL COMMENT 'north, south, east, west, northeast, northwest, southeast, southwest',
  `main_door_type` varchar(50) DEFAULT NULL COMMENT 'wooden, steel, glass, etc.',
  `main_door_width` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `main_door_height` decimal(5,2) DEFAULT NULL COMMENT 'in meters',
  `bedroom_door_type` varchar(50) DEFAULT NULL,
  `bathroom_door_type` varchar(50) DEFAULT NULL,
  `window_type` varchar(50) DEFAULT NULL COMMENT 'sliding, casement, french, etc.',
  `window_material` varchar(50) DEFAULT NULL COMMENT 'aluminum, upvc, wooden, etc.',
  `total_units` int DEFAULT '0',
  `available_units` int DEFAULT '0',
  `sold_units` int DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`unit_type_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `unit_types_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit_types`
--

LOCK TABLES `unit_types` WRITE;
/*!40000 ALTER TABLE `unit_types` DISABLE KEYS */;
INSERT INTO `unit_types` VALUES (1,1,'2 BHK Premium',2,2,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,1050.00,1250.00,1450.00,NULL,15000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(2,1,'3 BHK Luxury',3,3,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,1550.00,1850.00,2100.00,NULL,22000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(3,1,'4 BHK Ultra Luxury',4,4,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,2200.00,2600.00,2900.00,NULL,30000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(4,2,'3 BHK Classic',3,3,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,1650.00,1950.00,2200.00,NULL,18000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(5,2,'3 BHK Premium',3,3,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,1800.00,2100.00,2400.00,NULL,25000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(6,2,'4 BHK Luxury',4,4,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,2400.00,2800.00,3100.00,NULL,35000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(7,3,'3 BHK Ultra Luxury',3,3,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,2100.00,2400.00,2700.00,NULL,25000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(8,3,'4 BHK Premium',4,4,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,2800.00,3200.00,3600.00,NULL,35000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07'),(9,3,'4 BHK Penthouse',4,5,0,0,0,0,1,0,1,0,0,0,0,NULL,0,1,0,NULL,0,NULL,0,NULL,3500.00,4000.00,4500.00,NULL,50000000.00,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,0,1,'2025-07-16 05:53:07');
/*!40000 ALTER TABLE `unit_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_interests`
--

DROP TABLE IF EXISTS `user_interests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_interests` (
  `interest_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `project_id` int DEFAULT NULL,
  `unit_type_id` int DEFAULT NULL,
  `interest_type` varchar(20) NOT NULL COMMENT 'enquiry, site_visit, callback, brochure_download, price_quote',
  `preferred_contact_method` varchar(20) DEFAULT 'phone' COMMENT 'phone, email, whatsapp',
  `preferred_contact_time` varchar(20) DEFAULT 'anytime' COMMENT 'morning, afternoon, evening, anytime',
  `budget_min` decimal(15,2) DEFAULT NULL,
  `budget_max` decimal(15,2) DEFAULT NULL,
  `preferred_floors` text COMMENT 'comma separated',
  `specific_requirements` text,
  `status` varchar(30) DEFAULT 'new' COMMENT 'new, contacted, site_visit_scheduled, site_visit_done, negotiating, closed_won, closed_lost',
  `assigned_to` int DEFAULT NULL COMMENT 'agent user_id',
  `notes` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`interest_id`),
  KEY `user_id` (`user_id`),
  KEY `project_id` (`project_id`),
  KEY `unit_type_id` (`unit_type_id`),
  KEY `assigned_to` (`assigned_to`),
  CONSTRAINT `user_interests_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `user_interests_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `projects` (`project_id`),
  CONSTRAINT `user_interests_ibfk_3` FOREIGN KEY (`unit_type_id`) REFERENCES `unit_types` (`unit_type_id`),
  CONSTRAINT `user_interests_ibfk_4` FOREIGN KEY (`assigned_to`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_interests`
--

LOCK TABLES `user_interests` WRITE;
/*!40000 ALTER TABLE `user_interests` DISABLE KEYS */;
INSERT INTO `user_interests` VALUES (4,1,3,5,'q','qq','qqq',1.00,12.00,'1','q','q',1,'q','2025-07-23 00:19:03');
/*!40000 ALTER TABLE `user_interests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `user_type` varchar(20) DEFAULT 'buyer' COMMENT 'buyer, seller, agent, admin',
  `is_verified` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  `profile_image_url` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'abc.123@gmail.com','1234567891','Hi@123','ABC','ABD','custoomer',1,'2025-07-16 05:21:17',NULL,'',1,0),(3,'abc.1234@gmail.com',NULL,'pbkdf2:sha256:600000$VGrpf2ktzzTFQpBm$574423fe46d37db2fdc7335a6c51f9d4134508bd42106eef815399713da8409a','Priyanshu','Patel','buyer',0,'2025-07-22 00:26:59',NULL,NULL,1,0),(4,'abc.12345@gmail.com',NULL,'pbkdf2:sha256:600000$LP2lSCA6hcfYXnZS$afb517562c573691cb6d4b74e0d39395873dc9cef9f0458eb621cadcc9285cd8','Priyanshu','Patel','buyer',0,'2025-07-22 00:32:57',NULL,NULL,1,1),(5,'abd.123@gmail.com',NULL,'pbkdf2:sha256:600000$prVPGhGf5ZTFnr8u$b4080616eeee38652059403ea6d6aa87d91a15bc2a4363ac1af6b4e5f81a7edb','Harshal','Joshi','buyer',0,'2025-07-22 02:39:13',NULL,NULL,1,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-28 18:21:58
