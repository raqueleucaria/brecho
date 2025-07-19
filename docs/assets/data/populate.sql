-- -----------     << Brecho >>     -------------------
-- 
--                 POPULATE SCRIPT
-- 
-- Creation Date ..........: 07/07/2025
-- Author(s) ..............: Raquel Eucaria
-- Database ...............: MySQL 8.0
-- Database (name) ........: db_brecho
-- 
--
-- PROJETO => 01 Base de Dados
--         => 17 Tabelas

-- 
-- Last Changes
--   07/07/2025 => Criação do script de popula

-- -----------------------------------------------------------------

USE `db_brecho`;

-- -----------------------------------------------------

-- -----------------------------------------------------
-- Table `db_brecho`.`tbl_category`
-- -----------------------------------------------------

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
