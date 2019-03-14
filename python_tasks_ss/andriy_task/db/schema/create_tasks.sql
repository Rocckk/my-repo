-- this is the script for creation of table `tasks`

create table `tasks`(
`id` int unsigned not null auto_increment primary key,
`name` varchar(100),
`description` text,
`status` varchar(50),
check(`status` in('taken', 'free'))
)
engine InnoDB
default charset utf8
