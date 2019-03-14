--  this script creates table `clients`

create table `clients`(
`id` int unsigned not null auto_increment primary key,
`name` varchar(100),
`status` varchar(20),
check(`status` in ('busy', 'free')),
unique (`name`)
)
default charset utf8
engine InnoDB
