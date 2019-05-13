-- schema for creating table groups
CREATE TABLE `groups`(
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`name` VARCHAR(100),
`description` VARCHAR(300),
PRIMARY KEY (`id`)
)ENGINE InnoDB DEFAULT CHARSET=utf8;