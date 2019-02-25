-- script for populating `department_heads` table

insert into `department_heads` (teacher_id, department_id) values
((select id from `departments` where name = 'English Philology'), (select id from `teachers` where last_name = 'Bilynsky'));
