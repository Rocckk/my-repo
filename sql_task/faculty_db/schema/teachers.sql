-- table structure for the table `teachers`

create table `teachers`(
`id` int unsigned not null auto_increment,
`first_name` varchar(70),
`last_name` varchar(70),
`position` varchar(100),
`degree` varchar(100),
`academic_status` varchar(100),
`phone` varchar(50),
`department_id` int unsigned,
primary key (`id`),
foreign key (`department_id`) references `departments`(`id`)
on delete cascade
on update cascade
)
default charset utf8
;
