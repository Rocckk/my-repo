-- table structure for the table `subjects`

create table `subjects`(
`id` int unsigned not null auto_increment, 
`name` varchar(100),
`teacher_id` int unsigned,
primary key (`id`),
foreign key (`teacher_id`) references `teachers` (`id`)
on delete cascade
)
default charset utf8
;
