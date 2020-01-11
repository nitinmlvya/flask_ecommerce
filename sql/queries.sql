CREATE DATABASE `flask_db`;

CREATE TABLE `flask_db`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(64) NULL,
  `email` VARCHAR(120) NULL,
  `password` VARCHAR(128) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `usercol_UNIQUE` (`username` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC));

CREATE TABLE `flask_db`.`user_details` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(64) NULL,
  `user_id` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `id_idx` (`user_id` ASC),
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `flask_db`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);
