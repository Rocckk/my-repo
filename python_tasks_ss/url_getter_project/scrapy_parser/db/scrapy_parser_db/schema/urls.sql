-- schema for creation of table `urls`

CREATE TABLE `urls`(
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`url` VARCHAR(250) DEFAULT NULL COMMENT 'the URL which was found on the scraped web page',
primary key(`id`)
)ENGINE InnoDB DEFAULT CHARSET=utf8;
