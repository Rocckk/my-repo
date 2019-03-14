-- this script creates table `results`

create table `results`(
`task_id` int unsigned not null,
`client_id` int unsigned not null,
`result` varchar(50),
`output` text,
`start_time` datetime,
`end_time` datetime,
foreign key(`task_id`) references `tasks`(`id`)
on delete cascade,
foreign key(`client_id`) references `clients`(`id`)
on delete cascade,
check(`result` in('success', 'failure'))
)
engine InnoDB
default charset utf8
