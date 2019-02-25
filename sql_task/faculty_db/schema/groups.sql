-- table structure for the table `groups`

create table `groups`(
`id` int unsigned not null auto_increment,
`name` varchar(50),
`course` int unsigned,
`department_id` int unsigned,
`curator_is_teacher` int unsigned,
`groups_leader` int unsigned,
primary key (`id`),
foreign key (`department_id`) references `departments`(`id`)
on delete cascade
on update cascade,
foreign key (`curator_is_teacher`) references `teachers`(`id`)
on delete cascade
on update cascade 
)
default charset utf8
;
