-- this is the script for creation of table `tasks`

create table `tasks`(
`id` int unsigned not null auto_increment primary key,
`config` varchar(100),
`output` text,
`status` varchar(50),
`created` datetime,
`modified` datetime,
`job_type` int unsigned not null,
check(`status` in('new', 'in progress', 'done', 'error')),
check(`job_type` between 1 and 7)
)
engine InnoDB
default charset utf8
