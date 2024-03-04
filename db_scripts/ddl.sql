DROP DATABASE IF EXISTS expense_manager;

CREATE DATABASE expense_manager;

USE expense_manager;

DROP TABLE IF EXISTS `expense_manager`.`users`;
CREATE TABLE `expense_manager`.`users` (
  `user_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50),
  PRIMARY KEY (`user_id`));
  
DROP TABLE IF EXISTS `expense_manager`.`exp_groups`;
CREATE TABLE `expense_manager`.`exp_groups` (
  `group_id` INT NOT NULL,
  `group_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`group_id`));

DROP TABLE IF EXISTS `expense_manager`.`users_groups`;
CREATE TABLE `expense_manager`.`users_groups` (
  `user_id` INT NOT NULL,
  `group_id` INT NOT NULL,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `group_id_idx` (`group_id` ASC) VISIBLE,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `expense_manager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `expense_manager`.`exp_groups` (`group_id`)
    ON DELETE CASCADE);
    
DROP TABLE IF EXISTS `expense_manager`.`expenses`;
CREATE TABLE `expenses` (
  `expense_id` BIGINT NOT NULL,
  `group_id` int NOT NULL,
  `description` varchar(200) NOT NULL,
  `cost` float NOT NULL,
  `created_by` int NOT NULL,
  `created_at` date NOT NULL,
  `updated_by` int NOT NULL,
  `updated_at` date NOT NULL,
  PRIMARY KEY (`expense_id`),
  KEY `group_id_idx` (`group_id`),
  KEY `expenses_created_by_idx` (`created_by`),
  KEY `expenses_updated_by_idx` (`updated_by`),
  CONSTRAINT `expenses_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`),
  CONSTRAINT `expenses_group_id` FOREIGN KEY (`group_id`) REFERENCES `exp_groups` (`group_id`) ON DELETE CASCADE ON UPDATE NO ACTION
);

DROP TABLE IF EXISTS `expense_manager`.`repayments`;
CREATE TABLE `expense_manager`.`repayments` (
  `expense_id` BIGINT NOT NULL,
  `group_id` INT NOT NULL,
  `user_from` INT NOT NULL,
  `user_to` INT NOT NULL,
  `amount` FLOAT NOT NULL,
  INDEX `repayment_expense_id_idx` (`expense_id` ASC) VISIBLE,
  INDEX `repayment_group_id_idx` (`group_id` ASC) VISIBLE,
  INDEX `repayment_from_id_idx` (`user_from` ASC) VISIBLE,
  INDEX `repayment_to_id_idx` (`user_to` ASC) VISIBLE,
  CONSTRAINT `repayment_expense_id`
    FOREIGN KEY (`expense_id`)
    REFERENCES `expense_manager`.`expenses` (`expense_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `repayment_group_id`
    FOREIGN KEY (`group_id`)
    REFERENCES `expense_manager`.`exp_groups` (`group_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `repayment_from_id`
    FOREIGN KEY (`user_from`)
    REFERENCES `expense_manager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `repayment_to_id`
    FOREIGN KEY (`user_to`)
    REFERENCES `expense_manager`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
    
DROP TABLE IF EXISTS `expense_manager`.`shares`;
CREATE TABLE `shares` (
  `user_id` int NOT NULL,
  `expense_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `paid_share` float NOT NULL,
  `owed_share` float NOT NULL,
  `net_balance` float NOT NULL,
  KEY `shares_user_id_idx` (`user_id`),
  KEY `shares_group_id_idx` (`group_id`),
  KEY `shares_expense_id_idx` (`expense_id`),
  CONSTRAINT `shares_expense_id` FOREIGN KEY (`expense_id`) REFERENCES `expenses` (`expense_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `shares_group_id` FOREIGN KEY (`group_id`) REFERENCES `exp_groups` (`group_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `shares_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE NO ACTION
)