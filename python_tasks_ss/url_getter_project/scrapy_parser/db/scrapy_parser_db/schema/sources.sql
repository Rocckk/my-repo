-- schema for creation of table `sources`

CREATE TABLE `sources`(
`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
`url` VARCHAR(250) DEFAULT NULL COMMENT 'The URL of the scraped web page',
`count_of_urls` INT UNSIGNED DEFAULT NULL COMMENT 'The number of links found on the scraped web page',
PRIMARY KEY (`id`)
)ENGINE InnoDB DEFAULT CHARSET=utf8;
