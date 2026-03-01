-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: studentsurvey
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
INSERT INTO `accounts_customuser` VALUES (1,'pbkdf2_sha256$1200000$NtfMxS6ON1bJE7BbO11TUl$e0PU3x4B477YpVu37cVozrgK6mrZeP4ycYoDzFI+OU4=','2026-02-25 12:09:44.773323',1,'admin','','','admin@gmail.com',1,1,'2026-02-25 10:41:50.412240'),(2,'pbkdf2_sha256$1200000$ydvIvm0dKiIdQ0m33Q3OyV$8TWrmHwaD9GYTgTzGkFeuSP0MTmDvJE7GEIq4CriYS8=','2026-02-25 12:14:00.137901',0,'student','','','student@gmail.com',0,1,'2026-02-25 11:41:56.863862');
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser'),(25,'Can add survey',9,'add_survey'),(26,'Can change survey',9,'change_survey'),(27,'Can delete survey',9,'delete_survey'),(28,'Can view survey',9,'view_survey'),(29,'Can add question',7,'add_question'),(30,'Can change question',7,'change_question'),(31,'Can delete question',7,'delete_question'),(32,'Can view question',7,'view_question'),(33,'Can add rating',8,'add_rating'),(34,'Can change rating',8,'change_rating'),(35,'Can delete rating',8,'delete_rating'),(36,'Can view rating',8,'view_rating');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-02-25 11:59:13.069750','1','congTV',1,'[{\"added\": {}}, {\"added\": {\"name\": \"question\", \"object\": \"How satisfied are you with the teaching quality at your school?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How would you rate the availability of resources (books, technology, etc.) in your school?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How effective do you find the communication between teachers and students?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How safe do you feel while at school?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How well do you think the school promotes a positive learning environment?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How satisfied are you with the extracurricular activities offered?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How would you rate the school\'s facilities (classrooms, labs, sports areas)?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How approachable do you find the school administration?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How well does the school support students with different learning needs?\"}}, {\"added\": {\"name\": \"question\", \"object\": \"How likely are you to recommend this school to others?\"}}]',9,1),(2,'2026-02-25 12:06:46.104725','2','Student Satisfaction Survey: College of Information Systems',1,'[{\"added\": {}}, {\"added\": {\"name\": \"question\", \"object\": \"The curriculum is up-to-date with current industry trends (e.g., Cloud, AI, Data Science).\"}}, {\"added\": {\"name\": \"question\", \"object\": \"The balance between theoretical knowledge and practical technical skills is appropriate\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Course materials (textbooks, software, labs) are relevant and helpful for learning.\"}}, {\"added\": {\"name\": \"question\", \"object\": \"The sequence of courses follows a logical progression of difficulty.\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Instructors demonstrate a high level of expertise in their respective IS fields\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Faculty members are accessible for consultation and academic\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Grading and assessment methods are fair and transparent.\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Professors use effective teaching methods (e.g., hands-on coding, case studies).\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Computer laboratories are equipped with the necessary hardware and software\"}}, {\"added\": {\"name\": \"question\", \"object\": \"The campus Wi-Fi/Internet connectivity is reliable for research and projects.\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Study spaces and specialized IS libraries are adequate for student needs.\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Technical support services are responsive to student hardware/software issues.\"}}, {\"added\": {\"name\": \"question\", \"object\": \". The college provides sufficient internship and industry networking opportunities.\"}}, {\"added\": {\"name\": \"question\", \"object\": \". I feel confident that this program is preparing me for a career in Information System\"}}, {\"added\": {\"name\": \"question\", \"object\": \"Career services (job fairs, resume workshops) are effective and helpful\"}}]',9,1),(3,'2026-02-25 12:08:21.854016','26','HELLO',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','customuser'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(7,'survey','question'),(8,'survey','rating'),(9,'survey','survey');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-02-25 10:40:30.130787'),(2,'contenttypes','0002_remove_content_type_name','2026-02-25 10:40:30.193257'),(3,'auth','0001_initial','2026-02-25 10:40:30.348694'),(4,'auth','0002_alter_permission_name_max_length','2026-02-25 10:40:30.388096'),(5,'auth','0003_alter_user_email_max_length','2026-02-25 10:40:30.391793'),(6,'auth','0004_alter_user_username_opts','2026-02-25 10:40:30.395258'),(7,'auth','0005_alter_user_last_login_null','2026-02-25 10:40:30.398314'),(8,'auth','0006_require_contenttypes_0002','2026-02-25 10:40:30.399434'),(9,'auth','0007_alter_validators_add_error_messages','2026-02-25 10:40:30.403080'),(10,'auth','0008_alter_user_username_max_length','2026-02-25 10:40:30.405967'),(11,'auth','0009_alter_user_last_name_max_length','2026-02-25 10:40:30.409305'),(12,'auth','0010_alter_group_name_max_length','2026-02-25 10:40:30.417697'),(13,'auth','0011_update_proxy_permissions','2026-02-25 10:40:30.421533'),(14,'auth','0012_alter_user_first_name_max_length','2026-02-25 10:40:30.424811'),(15,'accounts','0001_initial','2026-02-25 10:40:30.603260'),(16,'admin','0001_initial','2026-02-25 10:40:30.686797'),(17,'admin','0002_logentry_remove_auto_add','2026-02-25 10:40:30.692517'),(18,'admin','0003_logentry_add_action_flag_choices','2026-02-25 10:40:30.696837'),(19,'sessions','0001_initial','2026-02-25 10:40:30.721889'),(20,'survey','0001_initial','2026-02-25 10:40:30.875280'),(21,'survey','0002_survey_description','2026-02-25 11:53:10.543309');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('s9shjwbnyotwsaec2rzbgo9hnkthoybp','.eJxVjDsOwjAQRO_iGlnB-EtJnzNYu-s1DiBbipMKcXcSKQVMOe_NvEWEdSlx7TzHKYmrUOL02yHQk-sO0gPqvUlqdZknlLsiD9rl2BK_bof7d1Cgl2191lYFf1FqYNA6G2cA0ZFLYQik2Bi23nIm3MIWMwOB9V5RTpw1gfh8AeeyOVw:1vvDmC:BqYxEbGEFLxmuHMyB_Zaz49PxChlDwgf6j6299sFUH0','2026-03-11 12:14:00.139721');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_question`
--

DROP TABLE IF EXISTS `survey_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` varchar(300) COLLATE utf8mb4_unicode_ci NOT NULL,
  `survey_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_question_survey_id_aa755a68_fk_survey_survey_id` (`survey_id`),
  CONSTRAINT `survey_question_survey_id_aa755a68_fk_survey_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `survey_survey` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_question`
--

LOCK TABLES `survey_question` WRITE;
/*!40000 ALTER TABLE `survey_question` DISABLE KEYS */;
INSERT INTO `survey_question` VALUES (1,'How satisfied are you with the teaching quality at your school?',1),(2,'How would you rate the availability of resources (books, technology, etc.) in your school?',1),(3,'How effective do you find the communication between teachers and students?',1),(4,'How safe do you feel while at school?',1),(5,'How well do you think the school promotes a positive learning environment?',1),(6,'How satisfied are you with the extracurricular activities offered?',1),(7,'How would you rate the school\'s facilities (classrooms, labs, sports areas)?',1),(8,'How approachable do you find the school administration?',1),(9,'How well does the school support students with different learning needs?',1),(10,'How likely are you to recommend this school to others?',1),(11,'The curriculum is up-to-date with current industry trends (e.g., Cloud, AI, Data Science).',2),(12,'The balance between theoretical knowledge and practical technical skills is appropriate',2),(13,'Course materials (textbooks, software, labs) are relevant and helpful for learning.',2),(14,'The sequence of courses follows a logical progression of difficulty.',2),(15,'Instructors demonstrate a high level of expertise in their respective IS fields',2),(16,'Faculty members are accessible for consultation and academic',2),(17,'Grading and assessment methods are fair and transparent.',2),(18,'Professors use effective teaching methods (e.g., hands-on coding, case studies).',2),(19,'Computer laboratories are equipped with the necessary hardware and software',2),(20,'The campus Wi-Fi/Internet connectivity is reliable for research and projects.',2),(21,'Study spaces and specialized IS libraries are adequate for student needs.',2),(22,'Technical support services are responsive to student hardware/software issues.',2),(23,'. The college provides sufficient internship and industry networking opportunities.',2),(24,'. I feel confident that this program is preparing me for a career in Information System',2),(25,'Career services (job fairs, resume workshops) are effective and helpful',2),(26,'HELLO',2);
/*!40000 ALTER TABLE `survey_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_rating`
--

DROP TABLE IF EXISTS `survey_rating`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_rating` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rating` int NOT NULL,
  `question_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `survey_rating_user_id_question_id_33c2671c_uniq` (`user_id`,`question_id`),
  KEY `survey_rating_question_id_5cda310a_fk_survey_question_id` (`question_id`),
  CONSTRAINT `survey_rating_question_id_5cda310a_fk_survey_question_id` FOREIGN KEY (`question_id`) REFERENCES `survey_question` (`id`),
  CONSTRAINT `survey_rating_user_id_e394208b_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_rating`
--

LOCK TABLES `survey_rating` WRITE;
/*!40000 ALTER TABLE `survey_rating` DISABLE KEYS */;
INSERT INTO `survey_rating` VALUES (1,1,1,2),(2,1,2,2),(3,1,3,2),(4,1,4,2),(5,1,5,2),(6,1,6,2),(7,5,7,2),(8,3,8,2),(9,1,9,2),(10,1,10,2);
/*!40000 ALTER TABLE `survey_rating` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `survey_survey`
--

DROP TABLE IF EXISTS `survey_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `survey_survey` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `survey_survey`
--

LOCK TABLES `survey_survey` WRITE;
/*!40000 ALTER TABLE `survey_survey` DISABLE KEYS */;
INSERT INTO `survey_survey` VALUES (1,'congTV','test'),(2,'Student Satisfaction Survey: College of Information Systems','Thank you for participating in this survey. Your feedback is vital for the continuous improvement of the College of Information Systems (CIS). Please rate your level of agreement with the following statements based on your experience.\r\nRating Scale:\r\n1 – Strongly Disagree\r\n2 – Disagree\r\n3 – Neutral\r\n4 – Agree\r\n5 – Strongly Agree\r\nSection A: Curriculum & Learning Content');
/*!40000 ALTER TABLE `survey_survey` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-25 23:02:12
