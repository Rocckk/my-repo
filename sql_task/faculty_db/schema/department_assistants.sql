-- table structure for the table `department_assistants`

create table `department_assistants` (
`id` int unsigned not null auto_increment,
`department_id` int unsigned,
`student_id` int unsigned,
primary key (`id`),
foreign key (`department_id`) references `departments` (`id`)
on delete cascade
on update cascade,
foreign key (`student_id`) references `students` (`id`)
on delete cascade
on update cascade
)
default charset utf8
;
