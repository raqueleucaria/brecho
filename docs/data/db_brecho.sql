CREATE SCHEMA IF NOT EXISTS `db_brecho` DEFAULT CHARACTER SET utf8mb4 ;
USE `db_brecho` ;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(255) NOT NULL,
  `user_nickname` VARCHAR(255) NOT NULL UNIQUE,
  `user_email` VARCHAR(255) NOT NULL UNIQUE,
  `user_password` VARCHAR(255) NOT NULL,
  `user_created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `user_updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;