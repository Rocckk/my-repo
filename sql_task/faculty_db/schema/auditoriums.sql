-- table structure for table `auditoriums`

create table `auditoriums`(
`id` int unsigned not null auto_increment,
`number` int unsigned not null,
`building` varchar (50),
primary key (`id`)
)
default character set utf8
;
