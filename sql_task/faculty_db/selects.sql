
-- query to select currently available auditoriums: no groups are associated with this auditorium and current time is not within some lesson's time frame

 select auditorium_id from lessons where current_time() < start_time or current_time() > end_time;


-- query to find out which teachers have lessons in group 'ink31' and when these lessons take place

select teachers.first_name, teachers.last_name, lessons.start_time, lessons.end_time from teachers join lessons on teachers.id = lessons.teacher_id join `groups` on lessons.groups_id = `groups`.id where `groups`.name = 'ink31';


-- query to figure out who works in the department 'Classical Philology'

select teachers.first_name, teachers.last_name from teachers join departments on teachers.department_id = departments.id where departments.name = 'Classical Philology';


-- find out the name of teachers who are members of faculty's council

 select teachers.first_name, teachers.last_name from teachers join teachers_roles on teachers.id = teachers_roles.teacher_id join administrative_roles on administrative_roles.id = teachers_roles.role_id where administrative_roles.role_name = 'Council member';

-- find out in which group some student studies (student with the last name 'Demyd')

select `groups`.name from students join `groups` on students.groups_id = `groups`.id where students.last_name = 'Demyd';


-- find out how many lessons in the form of lecture group 'ink31' has:

select * from lessons; select count(groups_id) num from `lessons` join `groups` on lessons.groups_id = `groups`.id where `groups`.name = 'ink31' and lessons.seminar_or_lecture = 'lecture';


