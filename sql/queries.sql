CREATE DATABASE `flask_db` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE `flask_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NULL,
  `email` VARCHAR(120) NULL,
  `password` VARCHAR(128) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `usercol_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));
