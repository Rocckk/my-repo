-- table structure for the table `students`

create table `students`(
`id` int unsigned not null auto_increment,
`first_name` varchar(70),
`last_name` varchar(70),
`groups_id` int unsigned,
`group_leader` int unsigned,
primary key (`id`),
foreign key (`groups_id`) references `groups` (`id`)
on delete cascade
)
default charset utf8
;

-- now we connect table `groups` with this table to be able to set group leaders


alter table `groups`
add foreign key (`groups_leader`) references students (id); 
