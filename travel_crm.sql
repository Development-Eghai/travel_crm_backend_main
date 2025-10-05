-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 28, 2025 at 05:48 AM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travel_crm`
--

-- --------------------------------------------------------

--
-- Table structure for table `activities`
--

DROP TABLE IF EXISTS `activities`;
CREATE TABLE IF NOT EXISTS `activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` text,
  `image` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activities`
--

INSERT INTO `activities` (`id`, `name`, `slug`, `description`, `image`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'River Raftingsfsdfvsd', 'river-rafting', 'Thrilling white-water adventure', 'https://cdn.example.com/rafting.jpg', 1, '2025-08-29 18:29:46', '2025-08-29 18:29:46'),
(2, 'Club', 'adventure', 'Thrilling white-water adventure', 'https://cdn.example.com/rafting.jpg', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55');

-- --------------------------------------------------------

--
-- Table structure for table `activity_types`
--

DROP TABLE IF EXISTS `activity_types`;
CREATE TABLE IF NOT EXISTS `activity_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `icon_url` text,
  `tenant_id` int NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activity_types`
--

INSERT INTO `activity_types` (`id`, `name`, `description`, `icon_url`, `tenant_id`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Adventure', 'High-energy activities like trekking, rafting, and ziplining', 'https://cdn.wanderpro.com/icons/adventure.png', 1, 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `api_keys`
--

DROP TABLE IF EXISTS `api_keys`;
CREATE TABLE IF NOT EXISTS `api_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `key_value` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tenant_id` int NOT NULL,
  `user_id` int NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `revoked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_value` (`key_value`),
  KEY `idx_api_keys_user_id` (`user_id`),
  KEY `idx_api_keys_key_value` (`key_value`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `api_keys`
--

INSERT INTO `api_keys` (`id`, `key_value`, `label`, `tenant_id`, `user_id`, `is_active`, `created_at`, `revoked_at`) VALUES
(1, 'bS8WV0lnLRutJH-NbUlYrO003q30b_f8B4VGYy9g45M', 'Auto-generated for anand@example.com', 1, 1, 1, '2025-08-29 13:00:25', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `blog_categories`
--

DROP TABLE IF EXISTS `blog_categories`;
CREATE TABLE IF NOT EXISTS `blog_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` text,
  `image_url` text,
  `parent_id` int DEFAULT NULL,
  `tenant_id` int NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `sort_order` int DEFAULT '0',
  `level` int DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `blog_categories`
--

INSERT INTO `blog_categories` (`id`, `name`, `slug`, `description`, `image_url`, `parent_id`, `tenant_id`, `is_active`, `sort_order`, `level`, `created_at`, `updated_at`) VALUES
(1, 'Adventure', 'adventure', 'Outdoor and thrill-seeking travel blogs', 'https://cdn.wanderpro.com/images/adventure.jpg', 1, 1, 1, 1, 0, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `blog_posts`
--

DROP TABLE IF EXISTS `blog_posts`;
CREATE TABLE IF NOT EXISTS `blog_posts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `heading` varchar(255) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `featured_image` text,
  `alt_tag` text,
  `date` date DEFAULT NULL,
  `author_name` varchar(255) DEFAULT NULL,
  `tag_ids` json DEFAULT NULL,
  `is_featured` tinyint(1) DEFAULT NULL,
  `is_published` tinyint(1) DEFAULT '0',
  `description` text,
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_tag` text,
  `meta_description` text,
  `slug` varchar(255) DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `blog_posts`
--

INSERT INTO `blog_posts` (`id`, `heading`, `category_id`, `featured_image`, `alt_tag`, `date`, `author_name`, `tag_ids`, `is_featured`, `is_published`, `description`, `meta_title`, `meta_tag`, `meta_description`, `slug`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Top 10 Beaches in South India', 3, 'https://cdn.wanderpro.com/blogs/beaches.jpg', 'Sunset at Kovalam Beach', '2025-08-22', 'Anand', '[1, 5, 9]', 1, 1, 'Explore the most serene and scenic beaches across Tamil Nadu and Kerala.', 'Best Beaches in South India', 'beach, travel, south india', 'A curated list of top beach destinations for your next coastal getaway.', 'best-beaches-south-india', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `blog_tags`
--

DROP TABLE IF EXISTS `blog_tags`;
CREATE TABLE IF NOT EXISTS `blog_tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
CREATE TABLE IF NOT EXISTS `bookings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(255) DEFAULT NULL,
  `trip_id` int DEFAULT NULL,
  `booking_type` enum('Fixed Departure','Customized') DEFAULT NULL,
  `booking_status` enum('Pending','Confirmed','Cancelled') DEFAULT NULL,
  `payment_status` enum('Pending','Paid','Refunded') DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `customer_name`, `trip_id`, `booking_type`, `booking_status`, `payment_status`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Ananya Rao', 4, 'Fixed Departure', 'Confirmed', 'Paid', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE IF NOT EXISTS `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` text,
  `image` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `slug`, `description`, `image`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Adventuredcc', 'adventure', 'Trips focused on thrill and outdoor activities', 'https://cdn.example.com/adventure.jpg', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47'),
(2, 'Paradice', 'adventure', 'Trips focused on thrill and outdoor activities', 'https://cdn.example.com/adventure.jpg', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55');

-- --------------------------------------------------------

--
-- Table structure for table `custom_packages`
--

DROP TABLE IF EXISTS `custom_packages`;
CREATE TABLE IF NOT EXISTS `custom_packages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `custom_packages`
--

INSERT INTO `custom_packages` (`id`, `destination_id`, `title`, `description`) VALUES
(19, 10, 'Exclusive Honeymoon Package', 'Romantic getaways in Kerala, Goa, and Udaipur.'),
(20, 10, 'Spiritual Retreats', 'Meditation and temple tours in Rishikesh and Varanasi.');

-- --------------------------------------------------------

--
-- Table structure for table `custom_package_trips`
--

DROP TABLE IF EXISTS `custom_package_trips`;
CREATE TABLE IF NOT EXISTS `custom_package_trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `package_id` int DEFAULT NULL,
  `trip_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `package_id` (`package_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `custom_package_trips`
--

INSERT INTO `custom_package_trips` (`id`, `package_id`, `trip_id`) VALUES
(28, 19, 103),
(29, 19, 104),
(30, 20, 105);

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

DROP TABLE IF EXISTS `destinations`;
CREATE TABLE IF NOT EXISTS `destinations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subtitle` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `destination_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `primary_destination_id` int DEFAULT NULL,
  `slug` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `overview` text COLLATE utf8mb4_unicode_ci,
  `travel_guidelines` text COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `idx_destinations_id` (`id`),
  KEY `primary_destination_id` (`primary_destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`id`, `title`, `subtitle`, `destination_type`, `primary_destination_id`, `slug`, `overview`, `travel_guidelines`, `created_at`, `updated_at`) VALUES
(10, 'India', 'India: A Land of Diversity and Culture555', 'Domestic', NULL, 'india', 'Explore the vibrant landscapes, rich heritage, and spiritual depth of India. From the Himalayas to the beaches of Goa, every corner offers a unique experience.', 'Carry valid ID proof. Follow local COVID protocols. Respect cultural norms.', '2025-09-23 16:35:04', '2025-09-23 16:35:04');

-- --------------------------------------------------------

--
-- Table structure for table `destination_activities`
--

DROP TABLE IF EXISTS `destination_activities`;
CREATE TABLE IF NOT EXISTS `destination_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `activity_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destination_activities`
--

INSERT INTO `destination_activities` (`id`, `destination_id`, `activity_id`) VALUES
(19, 10, 401),
(20, 10, 402);

-- --------------------------------------------------------

--
-- Table structure for table `destination_blogs`
--

DROP TABLE IF EXISTS `destination_blogs`;
CREATE TABLE IF NOT EXISTS `destination_blogs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `blog_id` int DEFAULT NULL,
  `featured` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destination_blogs`
--

INSERT INTO `destination_blogs` (`id`, `destination_id`, `blog_id`, `featured`) VALUES
(28, 10, 301, 1),
(29, 10, 302, 0),
(30, 10, 303, 0);

-- --------------------------------------------------------

--
-- Table structure for table `destination_blog_categories`
--

DROP TABLE IF EXISTS `destination_blog_categories`;
CREATE TABLE IF NOT EXISTS `destination_blog_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destination_blog_categories`
--

INSERT INTO `destination_blog_categories` (`id`, `destination_id`, `category_id`) VALUES
(19, 10, 201),
(20, 10, 202);

-- --------------------------------------------------------

--
-- Table structure for table `destination_testimonials`
--

DROP TABLE IF EXISTS `destination_testimonials`;
CREATE TABLE IF NOT EXISTS `destination_testimonials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `testimonial_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destination_testimonials`
--

INSERT INTO `destination_testimonials` (`id`, `destination_id`, `testimonial_id`) VALUES
(19, 10, 501),
(20, 10, 502);

-- --------------------------------------------------------

--
-- Table structure for table `destination_trips`
--

DROP TABLE IF EXISTS `destination_trips`;
CREATE TABLE IF NOT EXISTS `destination_trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `destination_id` int DEFAULT NULL,
  `trip_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `destination_id` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `destination_trips`
--

INSERT INTO `destination_trips` (`id`, `destination_id`, `trip_id`) VALUES
(19, 10, 101),
(20, 10, 102);

-- --------------------------------------------------------

--
-- Table structure for table `fixed_departures`
--

DROP TABLE IF EXISTS `fixed_departures`;
CREATE TABLE IF NOT EXISTS `fixed_departures` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `description` text,
  `tenant_id` int NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_trip_id` (`trip_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fixed_departures`
--

INSERT INTO `fixed_departures` (`id`, `trip_id`, `title`, `start_date`, `end_date`, `description`, `tenant_id`, `created_at`, `updated_at`) VALUES
(2, 1, 'WanderOn Himalayan Escape', '2025-09-15 10:00:00', '2025-09-20 18:00:00', 'A 6-day fixed departure to the Himalayas', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `global_settings`
--

DROP TABLE IF EXISTS `global_settings`;
CREATE TABLE IF NOT EXISTS `global_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_title` varchar(255) DEFAULT NULL,
  `tagline` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `site_description` text,
  `logo_url` varchar(255) DEFAULT NULL,
  `favicon_url` varchar(255) DEFAULT NULL,
  `homepage_slider` text,
  `contact_email` varchar(255) DEFAULT NULL,
  `contact_phones` text,
  `business_address` text,
  `social_links` text,
  `google_map_link` varchar(255) DEFAULT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `account_number` varchar(100) DEFAULT NULL,
  `ifsc_code` varchar(50) DEFAULT NULL,
  `branch_name` varchar(100) DEFAULT NULL,
  `upi_ids` text,
  `qr_code_images` text,
  `quotation_format` varchar(100) DEFAULT NULL,
  `invoice_format` varchar(100) DEFAULT NULL,
  `header_menu` text,
  `footer_menu` text,
  `meta_title` varchar(255) DEFAULT NULL,
  `meta_description` text,
  `meta_tags` text,
  `og_title` varchar(255) DEFAULT NULL,
  `og_description` text,
  `og_image` varchar(255) DEFAULT NULL,
  `terms_conditions` text,
  `privacy_policy` text,
  `payment_terms` text,
  `cancellation_policy` text,
  `refund_policy` text,
  `email_incoming` text,
  `email_form_submitted` text,
  `email_quotation_sent` text,
  `email_invoice_sent` text,
  `email_lead_assigned` text,
  `email_payment_confirmation` text,
  `email_invoice_due` text,
  `email_trip_updates` text,
  `email_follow_up` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `global_settings`
--

INSERT INTO `global_settings` (`id`, `site_title`, `tagline`, `company_name`, `site_description`, `logo_url`, `favicon_url`, `homepage_slider`, `contact_email`, `contact_phones`, `business_address`, `social_links`, `google_map_link`, `bank_name`, `account_number`, `ifsc_code`, `branch_name`, `upi_ids`, `qr_code_images`, `quotation_format`, `invoice_format`, `header_menu`, `footer_menu`, `meta_title`, `meta_description`, `meta_tags`, `og_title`, `og_description`, `og_image`, `terms_conditions`, `privacy_policy`, `payment_terms`, `cancellation_policy`, `refund_policy`, `email_incoming`, `email_form_submitted`, `email_quotation_sent`, `email_invoice_sent`, `email_lead_assigned`, `email_payment_confirmation`, `email_invoice_due`, `email_trip_updates`, `email_follow_up`) VALUES
(1, 'Wanderlust CRM', 'Where journeys begin', 'Wanderlust Travels Pvt Ltd', 'A powerful CRM platform for travel businesses to manage leads, quotations, invoices, and more.', 'https://wanderlustcrm.com/assets/logo.png', 'https://wanderlustcrm.com/assets/favicon.ico', 'https://wanderlustcrm.com/assets/slider1.jpg,https://wanderlustcrm.com/assets/slider2.mp4', 'support@wanderlustcrm.com', '+91-9876543210,+91-9123456789', 'No. 45, Mount Road, Chennai, Tamil Nadu, India', 'https://facebook.com/wanderlustcrm,https://instagram.com/wanderlustcrm,https://linkedin.com/company/wanderlustcrm', 'https://maps.google.com/?q=Wanderlust+Travels+Chennai', 'HDFC Bank', '123456789012', 'HDFC0001234', 'Chennai Main', 'wanderlust@hdfcbank,crm@upi', 'https://wanderlustcrm.com/assets/qr1.png,https://wanderlustcrm.com/assets/qr2.png', 'Modern', 'Professional', '[{\"name\":\"Home\",\"url\":\"/\"},{\"name\":\"About\",\"url\":\"/about\"},{\"name\":\"Contact\",\"url\":\"/contact\"}]', '[{\"name\":\"Privacy\",\"url\":\"/privacy\"},{\"name\":\"Terms\",\"url\":\"/terms\"}]', 'Wanderlust CRM - Travel Business Platform', 'Manage your travel business with ease using Wanderlust CRM.', 'travel,crm,quotation,invoice,lead management', 'Wanderlust CRM', 'Your travel business, streamlined.', 'https://wanderlustcrm.com/assets/og-image.jpg', 'All bookings are subject to availability and confirmation.', 'We respect your privacy and do not share data with third parties.', '50% advance, balance before departure.', 'Full refund if cancelled 7 days prior.', 'Refunds processed within 7 working days.', 'Thank you for contacting Wanderlust CRM. We’ll get back to you shortly.', 'Your form has been submitted successfully.', 'Your quotation is ready. Please find the attached details.', 'Your invoice has been generated. Kindly review and proceed with payment.', 'A new lead has been assigned to you.', 'We’ve received your payment. Thank you!', 'Reminder: Your invoice is due soon.', 'Your trip itinerary has been updated.', 'Just checking in — let us know if you need any help.');

-- --------------------------------------------------------

--
-- Table structure for table `invoices`
--

DROP TABLE IF EXISTS `invoices`;
CREATE TABLE IF NOT EXISTS `invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int NOT NULL,
  `quotation_id` int DEFAULT NULL,
  `client_name` varchar(255) DEFAULT NULL,
  `client_email` varchar(255) DEFAULT NULL,
  `client_phone` varchar(50) DEFAULT NULL,
  `client_gst` varchar(50) DEFAULT NULL,
  `client_address` text,
  `invoice_number` varchar(191) DEFAULT NULL,
  `iinvoice_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `due_date` date DEFAULT NULL,
  `is_interstate` tinyint(1) DEFAULT '0',
  `subtotal` float DEFAULT NULL,
  `discount` float DEFAULT NULL,
  `taxable_amount` float DEFAULT NULL,
  `cgst` float DEFAULT NULL,
  `sgst` float DEFAULT NULL,
  `igst` float DEFAULT NULL,
  `total_amount` float DEFAULT NULL,
  `due_amount` float DEFAULT NULL,
  `template` varchar(255) DEFAULT NULL,
  `terms_and_conditions` text,
  `payment_terms` text,
  `cancellation_policy` text,
  `notes` text,
  `invoice_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `ix_invoices_id` (`id`),
  KEY `lead_id` (`lead_id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `invoices`
--

INSERT INTO `invoices` (`id`, `lead_id`, `quotation_id`, `client_name`, `client_email`, `client_phone`, `client_gst`, `client_address`, `invoice_number`, `iinvoice_date`, `due_date`, `is_interstate`, `subtotal`, `discount`, `taxable_amount`, `cgst`, `sgst`, `igst`, `total_amount`, `due_amount`, `template`, `terms_and_conditions`, `payment_terms`, `cancellation_policy`, `notes`, `invoice_date`) VALUES
(1, 1, 1, 'Ravi Kumar', 'ravi.kumar@example.com', '9876543210', '29ABCDE1234F1Z5', 'No. 12, Gandhi Street, Salem, Tamil Nadu', 'INV-20250925-1', '2025-09-25 12:35:31', '2025-10-05', 0, 59000, 2800, 56200, 6463, 6463, 0, 69126, 39126, 'Professional', 'Subject to weather and availability.', '50% advance, balance on arrival.', 'Full refund if cancelled 7 days prior.', 'Please carry valid ID proof during travel.', '2025-09-25');

-- --------------------------------------------------------

--
-- Table structure for table `invoice_items`
--

DROP TABLE IF EXISTS `invoice_items`;
CREATE TABLE IF NOT EXISTS `invoice_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int DEFAULT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `description` text,
  `hsn_code` varchar(50) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` float DEFAULT NULL,
  `discount` float DEFAULT NULL,
  `discount_type` varchar(20) DEFAULT NULL,
  `gst_percent` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `invoice_items`
--

INSERT INTO `invoice_items` (`id`, `invoice_id`, `item_name`, `description`, `hsn_code`, `quantity`, `unit_price`, `discount`, `discount_type`, `gst_percent`) VALUES
(1, 1, 'Manali Adventure Package', '5-day trip including rafting, trekking, and stay', '9985', 2, 28000, 5, 'percent', 5),
(2, 1, 'Travel Insurance', 'Comprehensive coverage for trip duration', '9997', 2, 1500, 0, 'amount', 18);

-- --------------------------------------------------------

--
-- Table structure for table `invoice_payments`
--

DROP TABLE IF EXISTS `invoice_payments`;
CREATE TABLE IF NOT EXISTS `invoice_payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `invoice_payments`
--

INSERT INTO `invoice_payments` (`id`, `invoice_id`, `amount`, `method`, `date`, `transaction_id`, `notes`) VALUES
(1, 1, 30000, 'UPI', '2025-09-25', 'TXN123456789', 'Advance payment received via UPI');

-- --------------------------------------------------------

--
-- Table structure for table `itineraries`
--

DROP TABLE IF EXISTS `itineraries`;
CREATE TABLE IF NOT EXISTS `itineraries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `day_number` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  `image_urls` text,
  `activities` text,
  `hotel_name` varchar(255) DEFAULT NULL,
  `meal_plan` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `trip_id` (`trip_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `itineraries`
--

INSERT INTO `itineraries` (`id`, `trip_id`, `day_number`, `title`, `description`, `image_urls`, `activities`, `hotel_name`, `meal_plan`, `created_at`, `updated_at`) VALUES
(11, 6, 1, 'Arrival at Coimbatore', 'Pickup from airport and transfer to Ooty hotel.', 'https://example.com/images/day1.jpg', 'Pickup,Hotel Check-in', 'Ooty Grand', 'Dinner', '2025-09-23 16:01:05', '2025-09-23 16:01:05'),
(12, 6, 2, 'Ooty Sightseeing', 'Visit Botanical Garden, Rose Garden, and Doddabetta Peak.', 'https://example.com/images/day2.jpg', 'Sightseeing,Photography', 'Ooty Grand', 'Breakfast,Dinner', '2025-09-23 16:01:05', '2025-09-23 16:01:05');

-- --------------------------------------------------------

--
-- Table structure for table `leads`
--

DROP TABLE IF EXISTS `leads`;
CREATE TABLE IF NOT EXISTS `leads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `mobile` varchar(255) NOT NULL,
  `destination_type` varchar(255) NOT NULL,
  `pickup` varchar(255) DEFAULT NULL,
  `drop` varchar(255) DEFAULT NULL,
  `travel_from` date DEFAULT NULL,
  `travel_to` date DEFAULT NULL,
  `adults` int DEFAULT NULL,
  `children` int DEFAULT NULL,
  `status` varchar(255) DEFAULT 'New',
  `priority` varchar(255) DEFAULT 'Medium',
  `assigned_to` int DEFAULT NULL,
  `follow_up_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `source` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_leads_id` (`id`),
  KEY `assigned_to` (`assigned_to`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `leads`
--

INSERT INTO `leads` (`id`, `name`, `email`, `mobile`, `destination_type`, `pickup`, `drop`, `travel_from`, `travel_to`, `adults`, `children`, `status`, `priority`, `assigned_to`, `follow_up_date`, `created_at`, `source`) VALUES
(1, 'Priya Sharma', 'priya.sharma@example.com', '9876543210', 'Beach', 'Chennai Airport', 'Goa Resort', '2025-10-15', '2025-10-20', 2, 1, 'New', 'High', 3, '2025-10-05', '2025-09-25 11:50:43', 'Website Enquiry'),
(2, 'Ravi Kumar', 'ravi.kumar@example.com', '9876543210', 'Adventure', 'Delhi Airport', 'Manali Resort', '2025-11-10', '2025-11-15', 2, 1, 'Contacted', 'High', 5, '2025-10-05', '2025-09-25 11:55:43', 'Instagram Ad'),
(3, 'Ravi Kumar', 'ravi.kumar@example.com', '9876543210', 'Adventure', 'Delhi Airport', 'Manali Resort', '2025-11-10', '2025-11-15', 2, 1, 'Contacted', 'High', 5, '2025-10-05', '2025-09-25 11:59:44', 'Instagram Ad'),
(4, 'Ravi Kumar', 'ravi.kumar@example.com', '9876543210', 'Adventure', 'Delhi Airport', 'Manali Resort', '2025-11-10', '2025-11-15', 2, 1, 'Contacted', 'High', 5, '2025-10-05', '2025-09-25 11:59:44', 'Instagram Ad'),
(5, 'Revi Kumar', 'ravi.kumar@example.com', '9876543210', 'Adventure', 'Delhi Airport', 'Manali Resort', '2025-11-10', '2025-11-15', 2, 1, 'Contacted', 'High', 5, '2025-10-05', '2025-09-25 12:02:26', 'Instagram Ad');

-- --------------------------------------------------------

--
-- Table structure for table `lead_assignments`
--

DROP TABLE IF EXISTS `lead_assignments`;
CREATE TABLE IF NOT EXISTS `lead_assignments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int DEFAULT NULL,
  `assigned_to` int DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `priority` enum('Low','Medium','High') DEFAULT NULL,
  `follow_up_date` date DEFAULT NULL,
  `comments` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lead_assignments`
--

INSERT INTO `lead_assignments` (`id`, `lead_id`, `assigned_to`, `due_date`, `priority`, `follow_up_date`, `comments`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2025-08-26', 'High', '2025-08-25', 'Call after 10 AM. Interested in Ladakh trip.', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `lead_comments`
--

DROP TABLE IF EXISTS `lead_comments`;
CREATE TABLE IF NOT EXISTS `lead_comments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int DEFAULT NULL,
  `user_name` varchar(255) NOT NULL,
  `comment` text,
  `commented_by` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lead_comments`
--

INSERT INTO `lead_comments` (`id`, `lead_id`, `user_name`, `comment`, `commented_by`, `created_at`) VALUES
(1, 2, '', 'Customer requested Ladakh itinerary with hotel upgrade.', 4, '2025-08-29 18:29:46'),
(4, 5, 'Akshay', 'Client prefers snow activities and scenic stays.', NULL, '2025-09-25 12:05:34'),
(5, 5, 'Akshay', 'Requested quotation by next Monday.', NULL, '2025-09-25 12:05:34');

-- --------------------------------------------------------

--
-- Table structure for table `lead_documents`
--

DROP TABLE IF EXISTS `lead_documents`;
CREATE TABLE IF NOT EXISTS `lead_documents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `uploaded_by` int DEFAULT NULL,
  `uploaded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_lead_documents_id` (`id`),
  KEY `lead_id` (`lead_id`),
  KEY `uploaded_by` (`uploaded_by`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `lead_documents`
--

INSERT INTO `lead_documents` (`id`, `lead_id`, `file_name`, `file_path`, `uploaded_by`, `uploaded_at`) VALUES
(2, 5, 'passport_revi.pdf', '/uploads/leads/passport_ravi.pdf', 5, '2025-09-25 11:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
CREATE TABLE IF NOT EXISTS `menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(255) DEFAULT NULL,
  `items` json DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `quotations`
--

DROP TABLE IF EXISTS `quotations`;
CREATE TABLE IF NOT EXISTS `quotations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int NOT NULL,
  `design` varchar(255) NOT NULL,
  `status` varchar(255) DEFAULT 'Draft',
  `amount` int DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_quotations_id` (`id`),
  KEY `lead_id` (`lead_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotations`
--

INSERT INTO `quotations` (`id`, `lead_id`, `design`, `status`, `amount`, `date`) VALUES
(1, 1, 'Modern', 'Sent', 85000, '2025-09-25 00:00:00'),
(2, 5, 'Modern', 'Sent', 85000, '2025-09-25 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_agents`
--

DROP TABLE IF EXISTS `quotation_agents`;
CREATE TABLE IF NOT EXISTS `quotation_agents` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_agents`
--

INSERT INTO `quotation_agents` (`id`, `quotation_id`, `name`, `email`, `contact`) VALUES
(1, 1, 'Akshay Rao', 'akshay.rao@travelcrm.com', '9876543210'),
(2, 2, 'Akshay Rao', 'akshay.rao@travelcrm.com', '9876543210');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_companies`
--

DROP TABLE IF EXISTS `quotation_companies`;
CREATE TABLE IF NOT EXISTS `quotation_companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mobile` varchar(255) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `licence` varchar(255) DEFAULT NULL,
  `logo_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_companies`
--

INSERT INTO `quotation_companies` (`id`, `quotation_id`, `name`, `email`, `mobile`, `website`, `licence`, `logo_url`) VALUES
(1, 1, 'Wanderlust Travels', 'info@wanderlust.com', '9123456789', 'https://wanderlust.com', 'TRVL-2025-IND', 'https://wanderlust.com/assets/logo.png'),
(2, 2, 'Wanderlust Travels', 'info@wanderlust.com', '9123456789', 'https://wanderlust.com', 'TRVL-2025-IND', 'https://wanderlust.com/assets/logo.png');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_costing`
--

DROP TABLE IF EXISTS `quotation_costing`;
CREATE TABLE IF NOT EXISTS `quotation_costing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `price_per_person` int DEFAULT NULL,
  `price_per_package` int DEFAULT NULL,
  `selected_slot` varchar(255) DEFAULT NULL,
  `selected_package` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_costing`
--

INSERT INTO `quotation_costing` (`id`, `quotation_id`, `type`, `price_per_person`, `price_per_package`, `selected_slot`, `selected_package`) VALUES
(1, 1, 'customised', 28000, 85000, NULL, NULL),
(2, 2, 'customised', 28000, 85000, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `quotation_itinerary`
--

DROP TABLE IF EXISTS `quotation_itinerary`;
CREATE TABLE IF NOT EXISTS `quotation_itinerary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `day` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_itinerary`
--

INSERT INTO `quotation_itinerary` (`id`, `quotation_id`, `day`, `title`, `description`) VALUES
(1, 1, 1, 'Arrival & Welcome', 'Pickup from Delhi, scenic drive to Manali, welcome dinner.'),
(2, 1, 2, 'Adventure Day', 'River rafting and guided snow trek.'),
(3, 2, 1, 'Arrival & Welcome', 'Pickup from Delhi, scenic drive to Manali, welcome dinner.'),
(4, 2, 2, 'Adventure Day', 'River rafting and guided snow trek.');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_payment`
--

DROP TABLE IF EXISTS `quotation_payment`;
CREATE TABLE IF NOT EXISTS `quotation_payment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `bank_name` varchar(255) DEFAULT NULL,
  `account_number` varchar(255) DEFAULT NULL,
  `ifsc_code` varchar(255) DEFAULT NULL,
  `branch_name` varchar(255) DEFAULT NULL,
  `gst_number` varchar(255) DEFAULT NULL,
  `address` text,
  `upi_ids` text,
  `qr_code_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_payment`
--

INSERT INTO `quotation_payment` (`id`, `quotation_id`, `bank_name`, `account_number`, `ifsc_code`, `branch_name`, `gst_number`, `address`, `upi_ids`, `qr_code_url`) VALUES
(1, 1, 'HDFC Bank', '123456789012', 'HDFC0001234', 'Salem Main', '29ABCDE1234F1Z5', '123 MG Road, Salem, Tamil Nadu', 'akshayrao@hdfcbank,wanderlust@upi', 'https://wanderlust.com/assets/qr.png'),
(2, 2, 'HDFC Bank', '123456789012', 'HDFC0001234', 'Salem Main', '29ABCDE1234F1Z5', '123 MG Road, Salem, Tamil Nadu', 'akshayrao@hdfcbank,wanderlust@upi', 'https://wanderlust.com/assets/qr.png');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_policies`
--

DROP TABLE IF EXISTS `quotation_policies`;
CREATE TABLE IF NOT EXISTS `quotation_policies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `payment_terms` text,
  `cancellation_policy` text,
  `terms_and_conditions` text,
  `custom_policy` text,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_policies`
--

INSERT INTO `quotation_policies` (`id`, `quotation_id`, `payment_terms`, `cancellation_policy`, `terms_and_conditions`, `custom_policy`) VALUES
(1, 1, '50% advance, balance on arrival.', 'Full refund if cancelled 7 days prior.', 'Subject to weather and availability.', 'COVID protocols must be followed.'),
(2, 2, '50% advance, balance on arrival.', 'Full refund if cancelled 7 days prior.', 'Subject to weather and availability.', 'COVID protocols must be followed.');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_trips`
--

DROP TABLE IF EXISTS `quotation_trips`;
CREATE TABLE IF NOT EXISTS `quotation_trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `display_title` varchar(255) DEFAULT NULL,
  `overview` text,
  `hero_image` varchar(255) DEFAULT NULL,
  `gallery_images` text,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_trips`
--

INSERT INTO `quotation_trips` (`id`, `quotation_id`, `display_title`, `overview`, `hero_image`, `gallery_images`) VALUES
(1, 1, 'Manali Adventure Escape', 'A thrilling 5-day escape to the snowy peaks of Manali with curated adventure experiences.', 'https://wanderlust.com/trips/manali-hero.jpg', 'https://wanderlust.com/trips/gallery1.jpg,https://wanderlust.com/trips/gallery2.jpg'),
(2, 2, 'Manali Adventure Escape', 'A thrilling 5-day escape to the snowy peaks of Manali with curated adventure experiences.', 'https://wanderlust.com/trips/manali-hero.jpg', 'https://wanderlust.com/trips/gallery1.jpg,https://wanderlust.com/trips/gallery2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `quotation_trip_sections`
--

DROP TABLE IF EXISTS `quotation_trip_sections`;
CREATE TABLE IF NOT EXISTS `quotation_trip_sections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `quotation_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`),
  KEY `quotation_id` (`quotation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quotation_trip_sections`
--

INSERT INTO `quotation_trip_sections` (`id`, `quotation_id`, `title`, `content`) VALUES
(1, 1, 'Highlights', 'River rafting, snow trekking, bonfire nights.'),
(2, 1, 'FAQs', 'What to pack, safety measures, cancellation terms.'),
(3, 2, 'Highlights', 'River rafting, snow trekking, bonfire nights.'),
(4, 2, 'FAQs', 'What to pack, safety measures, cancellation terms.');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `modules` json DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `modules`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Sales Agent', '{\"leads\": true, \"bookings\": true, \"comments\": true, \"quotations\": false}', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `site_settings`
--

DROP TABLE IF EXISTS `site_settings`;
CREATE TABLE IF NOT EXISTS `site_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `site_title` varchar(255) DEFAULT NULL,
  `company_name` varchar(255) DEFAULT NULL,
  `site_description` text,
  `logo_url` text,
  `favicon_url` text,
  `contact_email` varchar(255) DEFAULT NULL,
  `phone_numbers` json DEFAULT NULL,
  `business_address` text,
  `tenant_id` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `site_settings`
--

INSERT INTO `site_settings` (`id`, `site_title`, `company_name`, `site_description`, `logo_url`, `favicon_url`, `contact_email`, `phone_numbers`, `business_address`, `tenant_id`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'WanderPro CRM', 'WanderPro Pvt Ltd', 'Your travel CRM for leads, bookings, and blogs', 'https://cdn.wanderpro.com/logo.png', 'https://cdn.wanderpro.com/favicon.ico', 'support@wanderpro.com', '{\"sales\": \"+91-9123456780\", \"support\": \"+91-9876543210\"}', '123, MG Road, Bengaluru', 1, 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE IF NOT EXISTS `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) DEFAULT NULL,
  `description` text,
  `tenant_id` int NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tags`
--

INSERT INTO `tags` (`id`, `name`, `slug`, `description`, `tenant_id`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Beach2', 'Beach2', 'All beach-related content and destinations', 1, 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE IF NOT EXISTS `tasks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `priority` enum('Low','Medium','High') DEFAULT NULL,
  `description` text,
  `assigned_to` int DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `status` enum('Pending','Completed') DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`id`, `title`, `priority`, `description`, `assigned_to`, `due_date`, `status`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Call client for itinerary confirmation', 'High', 'Confirm travel dates and send updated quotation', 1, '2025-08-24', 'Pending', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
CREATE TABLE IF NOT EXISTS `trips` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `overview` text,
  `destination_id` int NOT NULL,
  `destination_type` varchar(50) NOT NULL,
  `categories` text,
  `themes` text,
  `hotel_category` int DEFAULT NULL,
  `pickup_location` varchar(100) DEFAULT NULL,
  `drop_location` varchar(100) DEFAULT NULL,
  `days` int DEFAULT NULL,
  `nights` int DEFAULT NULL,
  `meta_tags` varchar(255) DEFAULT NULL,
  `slug` varchar(191) DEFAULT NULL,
  `pricing_model` varchar(50) DEFAULT NULL,
  `highlights` text,
  `inclusions` text,
  `exclusions` text,
  `faqs` text,
  `terms` text,
  `privacy_policy` text,
  `payment_terms` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trips`
--

INSERT INTO `trips` (`id`, `title`, `overview`, `destination_id`, `destination_type`, `categories`, `themes`, `hotel_category`, `pickup_location`, `drop_location`, `days`, `nights`, `meta_tags`, `slug`, `pricing_model`, `highlights`, `inclusions`, `exclusions`, `faqs`, `terms`, `privacy_policy`, `payment_terms`, `created_at`, `updated_at`) VALUES
(6, 'Trip to Ooty1', 'A scenic getaway to the Nilgiris with adventure and relaxation.', 101, 'Domestic', 'Family Packages,Group Packages', 'Nature,Adventure', 4, 'Coimbatore', 'Ooty', 5, 4, 'ooty, nature, family trip', 'trip-to-ooty', 'fixed', 'Tea gardens, boating, mountain views', 'Accommodation, breakfast, sightseeing', 'Lunch, personal expenses', 'Is this trip suitable for kids? Yes.', 'Full payment required before departure.', 'We do not share your data.', '50% advance, 50% before travel', '2025-09-23 16:01:05', '2025-09-23 16:01:05');

-- --------------------------------------------------------

--
-- Table structure for table `trips1`
--

DROP TABLE IF EXISTS `trips1`;
CREATE TABLE IF NOT EXISTS `trips1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `overview` text,
  `destination_id` int DEFAULT NULL,
  `trip_model` enum('Fixed','Custom') DEFAULT NULL,
  `trip_type_id` int DEFAULT NULL,
  `category_ids` json DEFAULT NULL,
  `hotel_category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `original_price` decimal(10,2) DEFAULT NULL,
  `pickup_location` varchar(255) DEFAULT NULL,
  `drop_location` varchar(255) DEFAULT NULL,
  `fixed_slots` json DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trips1`
--

INSERT INTO `trips1` (`id`, `title`, `overview`, `destination_id`, `trip_model`, `trip_type_id`, `category_ids`, `hotel_category`, `price`, `original_price`, `pickup_location`, `drop_location`, `fixed_slots`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Himalayan Adventure', 'Explore the majestic Himalayashgggggggg', 2, 'Fixed', 1, '[3, 5]', '3-Star', 12999.00, 14999.00, 'Delhi Airport', 'Delhi Airport', '[{\"end_date\": \"2025-10-07\", \"start_date\": \"2025-10-01\"}, {\"end_date\": \"2025-11-21\", \"start_date\": \"2025-11-15\"}]', 1, '2025-08-29 18:29:46', '2025-08-29 18:29:46'),
(2, 'Himalayan Adventure', 'Explore the majestic Himalayashgggggggg', 2, 'Fixed', 1, '[3, 5]', '3-Star', 12999.00, 14999.00, 'Delhi Airport', 'Delhi Airport', '[{\"end_date\": \"2025-10-07\", \"start_date\": \"2025-10-01\"}, {\"end_date\": \"2025-11-21\", \"start_date\": \"2025-11-15\"}]', 1, '2025-08-29 18:29:46', '2025-08-29 18:29:46'),
(3, 'holiday trip', 'good ', 1, 'Fixed', 1, '[]', '', 2500.00, 2000.00, 'Bangalore', 'goa', '[]', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55'),
(4, 'Enjoy Leave', 'Holiday trip', 1, 'Fixed', 1, '[]', '', 25000.00, 28000.00, 'Bangalore', 'goa', '[]', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55'),
(5, 'Bangkok holiday', 'Holiday', 2, 'Fixed', 2, '[1]', '', 35000.00, 40000.00, 'Bangalore', 'Bangkok', '[]', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55');

-- --------------------------------------------------------

--
-- Table structure for table `trip_days`
--

DROP TABLE IF EXISTS `trip_days`;
CREATE TABLE IF NOT EXISTS `trip_days` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int DEFAULT NULL,
  `day_title` varchar(255) DEFAULT NULL,
  `image_url` text,
  `description` text,
  `activity_ids` json DEFAULT NULL,
  `accommodation` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trip_days`
--

INSERT INTO `trip_days` (`id`, `trip_id`, `day_title`, `image_url`, `description`, `activity_ids`, `accommodation`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 4, 'Day 2 - Adventure Trek', 'https://cdn.example.com/day2.jpg', 'Morning trek followed by river rafting.', '[1]', 'Mountain Lodge', 1, '2025-08-29 18:29:47', '2025-08-29 18:29:47');

-- --------------------------------------------------------

--
-- Table structure for table `trip_details`
--

DROP TABLE IF EXISTS `trip_details`;
CREATE TABLE IF NOT EXISTS `trip_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int DEFAULT NULL,
  `highlights` text,
  `inclusions` text,
  `exclusions` text,
  `faqs` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trip_media`
--

DROP TABLE IF EXISTS `trip_media`;
CREATE TABLE IF NOT EXISTS `trip_media` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `hero_image_url` varchar(255) DEFAULT NULL,
  `thumbnail_url` varchar(255) DEFAULT NULL,
  `gallery_urls` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `trip_id` (`trip_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trip_media`
--

INSERT INTO `trip_media` (`id`, `trip_id`, `hero_image_url`, `thumbnail_url`, `gallery_urls`, `created_at`, `updated_at`) VALUES
(3, 6, 'https://example.com/images/hero.jpg', 'https://example.com/images/thumb.jpg', 'https://example.com/images/gallery1.jpg,https://example.com/images/gallery2.jpg', '2025-09-23 16:01:05', '2025-09-23 16:01:05');

-- --------------------------------------------------------

--
-- Table structure for table `trip_policies`
--

DROP TABLE IF EXISTS `trip_policies`;
CREATE TABLE IF NOT EXISTS `trip_policies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`),
  KEY `trip_id` (`trip_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trip_policies`
--

INSERT INTO `trip_policies` (`id`, `trip_id`, `title`, `content`) VALUES
(6, 6, 'Travel Insurance', 'Optional insurance available at extra cost.'),
(5, 6, 'Cancellation Policy', 'Full refund if cancelled 7 days before departure.');

-- --------------------------------------------------------

--
-- Table structure for table `trip_pricing`
--

DROP TABLE IF EXISTS `trip_pricing`;
CREATE TABLE IF NOT EXISTS `trip_pricing` (
  `id` int NOT NULL AUTO_INCREMENT,
  `trip_id` int NOT NULL,
  `pricing_model` varchar(50) DEFAULT NULL,
  `data` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `trip_id` (`trip_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trip_pricing`
--

INSERT INTO `trip_pricing` (`id`, `trip_id`, `pricing_model`, `data`, `created_at`) VALUES
(3, 6, 'fixed', '{\"pricing_model\": \"fixed\", \"fixed_departure\": [{\"from_date\": \"2025-09-25T00:00:00\", \"to_date\": \"2025-09-30T00:00:00\", \"available_slots\": 20, \"title\": \"Double Occupancy\", \"description\": \"Deluxe room for 2 adults\", \"base_price\": 15000.0, \"discount\": 2000.0, \"final_price\": 13000.0, \"booking_amount\": 8000.0, \"gst_percentage\": 5.0}]}', '2025-09-23 16:01:05');

-- --------------------------------------------------------

--
-- Table structure for table `trip_types`
--

DROP TABLE IF EXISTS `trip_types`;
CREATE TABLE IF NOT EXISTS `trip_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `description` text,
  `image` text,
  `tenant_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `trip_types`
--

INSERT INTO `trip_types` (`id`, `name`, `slug`, `description`, `image`, `tenant_id`, `created_at`, `updated_at`) VALUES
(1, 'Adventurefuiuy', 'adventure', 'Trips focused on outdoor and thrill activities', 'https://cdn.example.com/adventure.jpg', 1, '2025-08-29 18:29:46', '2025-08-29 18:29:46'),
(2, 'adventure nightlife', 'adventure', 'Trips focused on outdoor and thrill activities', 'https://cdn.example.com/adventure.jpg', 1, '2025-09-15 11:01:55', '2025-09-15 11:01:55');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `mobile_number` varchar(20) DEFAULT NULL,
  `password_hash` text,
  `role` enum('Admin','Editor','Agent') DEFAULT NULL,
  `send_user_email` tinyint(1) DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  `status` enum('Active','Inactive','Suspended') NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `api_key_count` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `first_name`, `last_name`, `mobile_number`, `password_hash`, `role`, `send_user_email`, `tenant_id`, `status`, `created_at`, `updated_at`, `api_key_count`) VALUES
(1, 'anand_dev', 'anand@example.com', 'Anand', 'Dev', '9876543210', '$2b$12$Iy2pXhvcFX0Y8Rd1aeZJY.VsNUh4Rfuc3yIBDQ.Uvq.UugII.sMYS', 'Admin', 0, 1, 'Active', '2025-08-29 13:00:25', '2025-08-29 13:00:25', 0);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `api_keys`
--
ALTER TABLE `api_keys`
  ADD CONSTRAINT `api_keys_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `custom_packages`
--
ALTER TABLE `custom_packages`
  ADD CONSTRAINT `custom_packages_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `custom_package_trips`
--
ALTER TABLE `custom_package_trips`
  ADD CONSTRAINT `custom_package_trips_ibfk_1` FOREIGN KEY (`package_id`) REFERENCES `custom_packages` (`id`);

--
-- Constraints for table `destinations`
--
ALTER TABLE `destinations`
  ADD CONSTRAINT `destinations_ibfk_1` FOREIGN KEY (`primary_destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `destination_activities`
--
ALTER TABLE `destination_activities`
  ADD CONSTRAINT `destination_activities_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `destination_blogs`
--
ALTER TABLE `destination_blogs`
  ADD CONSTRAINT `destination_blogs_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `destination_blog_categories`
--
ALTER TABLE `destination_blog_categories`
  ADD CONSTRAINT `destination_blog_categories_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `destination_testimonials`
--
ALTER TABLE `destination_testimonials`
  ADD CONSTRAINT `destination_testimonials_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `destination_trips`
--
ALTER TABLE `destination_trips`
  ADD CONSTRAINT `destination_trips_ibfk_1` FOREIGN KEY (`destination_id`) REFERENCES `destinations` (`id`);

--
-- Constraints for table `fixed_departures`
--
ALTER TABLE `fixed_departures`
  ADD CONSTRAINT `fixed_departures_ibfk_1` FOREIGN KEY (`trip_id`) REFERENCES `trips1` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
