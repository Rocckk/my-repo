-- table structure for the table `lessons`


create table `lessons`(
`start_time` time,
`end_time` time,
`auditorium_id` int unsigned,
`teacher_id` int unsigned,
`subject_id` int unsigned,
`groups_id` int unsigned,
`seminar_or_lecture` varchar (10),
foreign key (`auditorium_id`) references `auditoriums`(`id`)
on delete cascade
on update cascade,
foreign key (`teacher_id`) references `teachers`(`id`)
on delete cascade
on update cascade,
foreign key (`subject_id`) references `subjects`(`id`)
on delete cascade
on update cascade,
foreign key (`groups_id`) references `groups`(`id`)
on delete cascade
on update cascade
)
default charset utf8
;
