-- -----------     << Brecho >>     -------------------
-- 
--                 CREATION SCRIPT (DDL)
-- 
-- Creation Date ..........: 11/06/2025
-- Author(s) ..............: Raquel Eucaria
-- Database ...............: MySQL 8.0
-- Database (name) ........: db_brecho
-- 
--
-- PROJECT => 01 Database
--         => 15 Tables
-- 
-- Last Changes
--   11/06/2025 => Creation script created
--   07/07/2025 => Creation script completed
--   09/07/2025 => Refactored and updated tables structure

-- -----------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `db_brecho` DEFAULT CHARACTER SET utf8mb4 ;
CREATE DATABASE IF NOT EXISTS `db_brecho`;  

USE `db_brecho`;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_nickname` VARCHAR(255) NOT NULL UNIQUE,
  `user_email` VARCHAR(255) NOT NULL UNIQUE,
  `user_name` VARCHAR(255) NOT NULL,
  `user_password` VARCHAR(255) NOT NULL,
  `user_phone_country_code` VARCHAR(10) NOT NULL,
  `user_phone_state_code` VARCHAR(10) NOT NULL,
  `user_phone_number` VARCHAR(10) NOT NULL,
  
  CONSTRAINT USER_PK PRIMARY KEY (`user_id`)
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_address` (
  `address_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `address_country` VARCHAR(100) NOT NULL,
  `address_zip_code` VARCHAR(20) NOT NULL,
  `address_state` VARCHAR(100) NOT NULL,
  `address_city` VARCHAR(100) NOT NULL,
  `address_neighborhood` VARCHAR(100) NOT NULL,
  `address_street` VARCHAR(255) NOT NULL,
  `address_number` VARCHAR(10) NOT NULL,
  `address_complement` VARCHAR(255),
  `user_id` INT UNSIGNED NOT NULL,
  
  CONSTRAINT ADDRESS_PK PRIMARY KEY (`address_id`),
  CONSTRAINT ADDRESS_USER_FK FOREIGN KEY (`user_id`) REFERENCES `tbl_user` (`user_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_client` (
  `client_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,

  CONSTRAINT CLIENT_PK PRIMARY KEY (`client_id`),
  CONSTRAINT CLIENT_USER_FK FOREIGN KEY (`user_id`) REFERENCES `tbl_user`(`user_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_seller`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_seller` (
  `seller_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `seller_status` ENUM('active', 'inactive') NOT NULL DEFAULT 'inactive',
  `seller_description` VARCHAR(500),
  `seller_bank_account` VARCHAR(7) NOT NULL,
  `seller_bank_agency` VARCHAR(6) NOT NULL,
  `seller_bank_name` VARCHAR(100) NOT NULL,
  `seller_bank_type` ENUM('checking', 'savings') NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,

  CONSTRAINT SELLER_PK PRIMARY KEY (`seller_id`),
  CONSTRAINT SELLER_USER_FK FOREIGN KEY (`user_id`) REFERENCES `tbl_user`(`user_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_category` (
  `category_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(255) NOT NULL UNIQUE,

  CONSTRAINT CATEGORY_PK PRIMARY KEY (`category_id`)
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_color`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_color` (
  `color_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `color_name` VARCHAR(50) NOT NULL UNIQUE,

  CONSTRAINT COLOR_PK PRIMARY KEY (`color_id`)
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_product` (
  `product_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(100) NOT NULL,
  `product_description` VARCHAR(500),
  `product_price` DECIMAL(10,2) NOT NULL,
  `product_status` ENUM('available', 'unavailable') NOT NULL DEFAULT 'available',
  `product_image` VARCHAR(255),
  `product_condition` ENUM('new', 'used', 'refurbished') NOT NULL,
  `product_gender` ENUM('F', 'M', 'U') NOT NULL,
  `product_size` ENUM('XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', '34', '36', '38', '40', '42', '44', '46', '48') NOT NULL,
  `category_id` INT UNSIGNED NOT NULL,
  `color_id` INT UNSIGNED NOT NULL,
  `seller_id` INT UNSIGNED NOT NULL,

  CONSTRAINT PRODUCT_PK PRIMARY KEY (`product_id`),
  CONSTRAINT PRODUCT_CATEGORY_FK FOREIGN KEY (`category_id`) REFERENCES `tbl_category`(`category_id`) DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT PRODUCT_COLOR_FK FOREIGN KEY (`color_id`) REFERENCES `tbl_color`(`color_id`) DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT PRODUCT_SELLER_FK FOREIGN KEY (`seller_id`) REFERENCES `tbl_seller`(`seller_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_cart_want`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_cart_want` (
  `product_id` INT UNSIGNED NOT NULL,
  `client_id` INT UNSIGNED NOT NULL,
  `want_type` ENUM('cart', 'wishlist') NOT NULL,

  CONSTRAINT CART_WANT_PK PRIMARY KEY (`product_id`, `client_id`),
  CONSTRAINT CART_WANT_PRODUCT_FK FOREIGN KEY (`product_id`) REFERENCES `tbl_product`(`product_id`) DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT CART_WANT_CLIENT_FK FOREIGN KEY (`client_id`) REFERENCES `tbl_client`(`client_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.tbl_checkout
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_checkout` (
  `checkout_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `promotion` DECIMAL(10,2) NOT NULL,

  CONSTRAINT CHECKOUT_PK PRIMARY KEY (`checkout_id`)
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_generate`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_generate` (
  `checkout_id` INT UNSIGNED NOT NULL,
  `product_id` INT UNSIGNED NOT NULL,

  CONSTRAINT GENERATE_PK PRIMARY KEY (`checkout_id`, `product_id`, `client_id`),
  CONSTRAINT GENERATE_CHECKOUT_FK FOREIGN KEY (`checkout_id`) REFERENCES `tbl_checkout`(`checkout_id`) DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT GENERATE_PRODUCT_FK FOREIGN KEY (`product_id`) REFERENCES `tbl_product`(`product_id`) DELETE RESTRICT ON UPDATE RESTRICT,
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_analyse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_analyse` (
  `checkout_id` INT UNSIGNED NOT NULL,
  `address_id` INT UNSIGNED NOT NULL,
  `shipping_fee` DECIMAL(6,2) NOT NULL,

  CONSTRAINT ANALYSE_PK PRIMARY KEY (`checkout_id`, `address_id`),
  CONSTRAINT ANALYSE_CHECKOUT_FK FOREIGN KEY (`checkout_id`) REFERENCES `tbl_checkout`(`checkout_id`) DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT ANALYSE_ADDRESS_FK FOREIGN KEY (`address_id`) REFERENCES `tbl_address`(`address_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_order_payment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_order_payment` (
  `order_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `order_number` VARCHAR(50) NOT NULL UNIQUE,
  `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `order_status` ENUM('pending', 'paid', 'shipped', 'delivered', 'cancelled', 'expired') DEFAULT 'pending',
  `order_updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `payment_method` ENUM('credit_card', 'debit_card', 'bank_transfer', 'pix') NOT NULL,
  `payment_date` DATETIME,
  `order_tracking` ENUM('shipped', 'in_transit', 'delivered', 'returned') NOT NULL DEFAULT 'pending',
  `checkout_id` INT UNSIGNED NOT NULL,

  CONSTRAINT ORDER_PAYMENT_PK PRIMARY KEY (`order_id`),
  CONSTRAINT ORDER_PAYMENT_CHECKOUT_FK FOREIGN KEY (`checkout_id`) REFERENCES `tbl_checkout`(`checkout_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_card`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_card` (
  `card_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `card_number` VARCHAR(20) NOT NULL,
  `card_expiry_date` DATE NOT NULL,
  `card_holder_name` VARCHAR(100) NOT NULL,
  `card_holder_national_code` VARCHAR(20) NOT NULL,
  `order_payment_id` INT UNSIGNED NOT NULL,

  CONSTRAINT CARD_PK PRIMARY KEY (`card_id`),
  CONSTRAINT CARD_ORDER_PAYMENT_FK FOREIGN KEY (`order_payment_id`) REFERENCES `tbl_order_payment`(`order_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_pix`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_pix` (
  `pix_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pix_key` VARCHAR(255) NOT NULL UNIQUE,
  `pix_expiry_date` DATETIME NOT NULL,
  `order_payment_id` INT UNSIGNED NOT NULL,

  CONSTRAINT PIX_PK PRIMARY KEY (`pix_id`),
  CONSTRAINT PIX_ORDER_PAYMENT_FK FOREIGN KEY (`order_payment_id`) REFERENCES `tbl_order_payment`(`order_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_boleto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_boleto` (
  `boleto_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `boleto_bar_code` VARCHAR(255) NOT NULL UNIQUE,
  `boleto_expiry_date` DATE NOT NULL,
  `order_payment_id` INT UNSIGNED NOT NULL,

  CONSTRAINT BOLETO_PK PRIMARY KEY (`boleto_id`),
  CONSTRAINT BOLETO_ORDER_PAYMENT_FK FOREIGN KEY (`order_payment_id`) REFERENCES `tbl_order_payment`(`order_id`) DELETE RESTRICT ON UPDATE RESTRICT
)ENGINE = InnoDB;
