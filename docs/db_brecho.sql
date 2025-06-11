CREATE SCHEMA IF NOT EXISTS `db_brecho` DEFAULT CHARACTER SET utf8mb4 ;
USE `db_brecho` ;

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `db_brecho`.`tbl_user` (
  `user_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_nome` VARCHAR(255) NULL DEFAULT NULL,
  `user_email` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;