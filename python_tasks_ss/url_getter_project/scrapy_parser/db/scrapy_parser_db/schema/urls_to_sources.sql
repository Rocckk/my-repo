-- schema for creation of table `urls_to_sources`

CREATE TABLE `urls_to_sources` (
`source_id` INT UNSIGNED NOT NULL COMMENT 'The id of the source web page',
`url_id` INT UNSIGNED NOT NULL COMMENT 'The id of the url which was found on the source web page',
FOREIGN KEY(`source_id`) REFERENCES `sources`(`id`),
FOREIGN KEY(`url_id`) REFERENCES `urls`(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
