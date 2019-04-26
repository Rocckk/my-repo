-- schema for creation of table `sources`

create table `webpages`(

`id` int unsigned not null auto_increment,

`url` varchar(250) DEFAULT NULL,

`count_of_urls` int unsigned DEFAULT NULL,

primary key (`id`)
)

engine InnoDB

default charset utf8


