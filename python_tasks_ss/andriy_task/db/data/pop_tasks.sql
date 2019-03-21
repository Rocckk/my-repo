-- the script for populating table `tasks`

insert into `tasks` (`id`, `status`, `created`, `job_type`, `config`) values
(1, 'new', now(), 1, 'test_file.txt'),
(2, 'new', now(), 2, 'a.txt'),
(3, 'new', now(), 3, 'adir'),
(4, 'new', now(), 4, 'a.txt'),
(5, 'new', now(), 5, 'adir'),
(6, 'new', now(), 6, 'ls'),
(7, 'new', now(), 7, '3');
