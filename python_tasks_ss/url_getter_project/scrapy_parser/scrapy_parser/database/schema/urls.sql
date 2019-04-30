-- schema for creation of table `urls`

create table `urls`(

`id` int unsigned not null auto_increment,

`url` varchar(250) DEFAULT NULL,

primary key(`id`)
)

engine InnoDB

default charset utf8
