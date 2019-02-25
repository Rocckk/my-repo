-- table structure for the table `marks`

create table `marks`(
`mark` int unsigned,
`mark_date` date,
`student_id` int unsigned,
`subject_id` int unsigned,
foreign key (`subject_id`) references `subjects` (`id`)
on delete cascade
on update cascade,
foreign key (`student_id`) references `students` (`id`)
on delete cascade
on update cascade
)
default charset utf8
;
