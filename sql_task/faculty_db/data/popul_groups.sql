-- script populating `groups` table

insert into `groups` (name, course, department_id, curator_is_teacher, group_leader) values
('Ink31', 3, (select id from departments where name = 'Classical Philology'), 2, 1),
('Ink21', 2, (select id from departments where name = 'Classical Philology'), 3, 2),
('Ink41', 4, (select id from departments where name = 'Classical Philology'), 4, 3),
('Ink11', 1, (select id from departments where name = 'Classical Philology'), 5, 4),
('Ink51s', 5, (select id from departments where name = 'Classical Philology'), 6, 5),
('Ink61m', 6, (select id from departments where name = 'Classical Philology'), 7, 6),
('Inp31', 3, (select id from departments where name = 'English Philology'), 8, 7),
('Inp32', 3, (select id from departments where name = 'English Philology'), 9, 8),
('Inp33', 3, (select id from departments where name = 'English Philology'), 10, 9),
('Ina21', 2, (select id from departments where name = 'English Philology'), null, 10);

-- addition to the table `students` which could not be added when that table was being populated:

insert into `students` (`groups_id`) values
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);

