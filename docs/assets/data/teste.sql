USE `db_brecho`;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_user`
-- -----------------------------------------------------

-- INSERT INTO `tbl_user` (`user_id`, `user_nickname`, `user_email`, `user_name`, `user_password`, `user_phone_country_code`, `user_phone_state_code`, `user_phone_number`) VALUES
-- (1, 'user1_nick', 'user1@email.com', 'user1', 'password1', '+1', '123', '4567890'),
-- (2, 'user2_nick', 'user2@email.com', 'user2', 'password2', '+1', '234', '5678901'),
-- (3, 'user3_nick', 'user3@email.com', 'user3', 'password3', '+1', '345', '6789012'),
-- (4, 'user4_nick', 'user4@email.com', 'user4', 'password4', '+1', '456', '7890123'),
-- (5, 'user5_nick', 'user5@email.com', 'user5', 'password5', '+1', '567', '8901234');


{
  "user_name": "string",
  "user_nickname": "string",
  "user_email": "user@example.com",
  "user_password": "string",
  "user_phone_country_code": "string",
  "user_phone_state_code": "string",
  "user_phone_number": "string"
}

{
  "user_name": "user2",
  "user_nickname": "user2_nick",
  "user_email": "user@example2.com",
  "user_password": "password2",
  "user_phone_country_code": "+2",
  "user_phone_state_code": "234",
  "user_phone_number": "25678901"
}

{
  "user_name": "user3",
  "user_nickname": "user3_nick",
  "user_email": "user@example3.com",
  "user_password": "password3",
  "user_phone_country_code": "+3",
  "user_phone_state_code": "345",
  "user_phone_number": "346789012"
}


-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_seller`
-- -----------------------------------------------------

-- CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_seller` (
--   `seller_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
--   `seller_status` ENUM('active', 'inactive') NOT NULL DEFAULT 'inactive',
--   `seller_description` VARCHAR(500),
--   `seller_bank_account` VARCHAR(7) NOT NULL,
--   `seller_bank_agency` VARCHAR(6) NOT NULL,
--   `seller_bank_name` VARCHAR(100) NOT NULL,
--   `seller_bank_type` ENUM('checking', 'savings') NOT NULL,
--   `user_id` INT UNSIGNED NOT NULL,

--   CONSTRAINT SELLER_PK PRIMARY KEY (`seller_id`),
--   CONSTRAINT SELLER_USER_FK FOREIGN KEY (`user_id`) REFERENCES `tbl_user`(`user_id`) DELETE RESTRICT ON UPDATE RESTRICT
-- )ENGINE = InnoDB;

INSERT INTO `tbl_seller` (`seller_id`, `seller_status`, `seller_description`, `seller_bank_account`, `seller_bank_agency`, `seller_bank_name`, `seller_bank_type`, `user_id`) VALUES
(1, 'active', 'Seller 1 description', '1234567', '123456', 'Bank A', 'checking', 1),
(2, 'inactive', 'Seller 2 description', '2345678', '234567', 'Bank B', 'savings', 2);

-- -------------------------------------------------------
-- Table `db_brecho`.`tbl_category`

INSERT INTO `tbl_category` (`category_id`, `category_name`) VALUES
(1, 'Dresses'),
(2, 'T-shirts'),
(3, 'Pants'),
(4, 'Shoes'),
(5, 'Accessories'),
(6, 'Bags'),
(7, 'Jackets'),
(8, 'Skirts'),
(9, 'Shorts'),
(10, 'Sweaters'),
(11, 'Suits'),
(12, 'Hats'),
(13, 'Jewelry'),
(14, 'Sunglasses'),
(15, 'Belts');

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_color`
-- -----------------------------------------------------

INSERT INTO `tbl_color` (`color_id`, `color_name`) VALUES
(1, 'Red'),
(2, 'Blue'),
(3, 'Green'),
(4, 'Black'),
(5, 'White'),
(6, 'Yellow'),
(7, 'Pink'),
(8, 'Purple'),
(9, 'Orange'),
(10, 'Gray');
