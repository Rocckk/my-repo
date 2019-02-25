-- population script for table `lessons`


insert into `lessons` (start_time, end_time, auditorium_id, teacher_id, subject_id, groups_id, seminar_or_lecture) values
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 1), (select id from `teachers` where last_name = 'Sulym'), (select id from `subjects` where name = 'Audiovisual Translation'), (select id from `groups` where name = 'Ink31'), 'seminar'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 2), (select id from `teachers` where last_name = 'Hlushchenko'), (select id from `subjects` where name = 'Methodology of Teaching Latin Language'), (select id from `groups` where name = 'Ink21'), 'seminar'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 3), (select id from `teachers` where last_name = 'Kost'), (select id from `subjects` where name = 'French Stylistics'), null, 'lecture'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 4), (select id from `teachers` where last_name = 'Safronyak'), (select id from `subjects` where name = 'Old Greek Language and Authors'), (select id from `groups` where name = 'Ink41'), 'lecture'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 5), (select id from `teachers` where last_name = 'Safron'), (select id from `subjects` where name = 'Methodology of Teaching Latin Language'), (select id from `groups` where name = 'Ink51s'), 'lecture'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 6), (select id from `teachers` where last_name = 'Sodomora'), (select id from `subjects` where name = 'Old Greek Language and Authors'), (select id from `groups` where name = 'Ink61m'), 'lecture'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 7), (select id from `teachers` where last_name = 'Bilynsky'), (select id from `subjects` where name = 'History of the Language (English-Ukrainian Translation)'), (select id from `groups` where name = 'Inp31'), 'lecture'),
('08:00:00', '09:30:00', (select id from `auditoriums` where number = 8), (select id from `teachers` where last_name = 'Safronyan'), null, null, null),
('09:40:00', '11:10:00', (select id from `auditoriums` where number = 9), (select id from `teachers` where last_name = 'Sulym'), (select id from `subjects` where name = 'Audiovisual Translation'), null, null),
('09:40:00', '11:10:00', (select id from `auditoriums` where number = 10), (select id from `teachers` where last_name = 'Hlushchenko'), (select id from `subjects` where name = 'Methodology of Teaching Latin Language'), (select id from `groups` where name = 'Ink31'), 'seminar');
