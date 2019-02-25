-- script for populating `teachers` table


insert into `teachers` (first_name, last_name, position, degree, academic_status, phone, department_id) values
('Volodymyr', 'Sulym', 'Dean of Faculty of Foreign Languages', 'Candidate of Philological Sciences', 'Associate Professor', '(032) 239-46-80', (select id from `departments` where name = 'Intercultural Communication and Translation')),
('Lina', 'Hlushchenko', 'Associate Dean', 'Candidate of Philological Sciences', 'Associate Professor', '(032) 239-41-38', (select id from `departments` where name = 'Classical Philology')),
('Olha', 'Ivashchyshyn', 'Associate Dean', 'Candidate of Philological Sciences', 'Associate Professor', '(032) 239-47-16', (select id from `departments` where name = 'Foreign Languages for the Humanities')),
('Hanna', 'Kost', 'Associate Dean', 'Candidate of Philological Sciences', 'Associate Professor', '(032) 239-47-37', (select id from `departments` where name = 'French Philology')),
('Hanna', 'Safronyak', 'Associate Dean', 'Candidate of Philological Sciences', 'Associate Professor', '(032) 239-41-38', (select id from `departments` where name = 'Classical Philology')),
('Olha', 'Kisil', null, null, null, '(032) 239-42-14',null),
('Bohdan', 'Safron', 'Chairperson', 'Doctor of Philological Sciences', 'Associate Professor', '(032) 239-41-38', (select id from `departments` where name = 'Classical Philology')),
('Hanna', 'Sodomora', 'Professor', 'Candidate of Philological Sciences', 'Professor', '(032) 239-41-38', (select id from `departments`where name = 'Classical Philology')),
('Mykhailo', 'Bilynsky', 'Chairperson', 'Candidate of Philological Sciences', 'Professor', '(032) 239-41-04', (select id from `departments` where name = 'English Philology')),
('Natalya', 'Safronyan', 'Acting Chairperson', 'Doctor of Philological Sciences', 'Professor', '(032) 239-44-54', (select id from `departments` where name = 'Foreign Languages for Natural Sciences'));
