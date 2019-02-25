-- Table structure for table `departments`

create table `departments`(
`id` int unsigned not null auto_increment,
`name` varchar(100),
`phone` varchar(100),
`email` varchar(100),
primary key (`id`)
)
default charset utf8
;
