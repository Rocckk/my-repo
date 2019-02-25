-- table structure for the table `teachers_roles`

create table `teachers_roles`(
`role_id` int unsigned,
`teacher_id` int unsigned,
foreign key (`role_id`) references `administrative_roles` (`id`)
on delete cascade
on update cascade,
foreign key (`teacher_id`) references `teachers` (`id`)
on delete cascade
on update cascade
)
default charset utf8
;
