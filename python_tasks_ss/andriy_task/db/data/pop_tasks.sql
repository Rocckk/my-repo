-- the script for populating table `tasks`

insert into `tasks` (`name`, `description`, `status`) values
('uniqueness counter', 'count the unique words in a file', 'free'),
('file creator', 'create a file', 'free'),
('directory creator', 'create a directory', 'free'),
('file deleter', 'delete a file', 'free'),
('dir deleter', 'delete a directory', 'free'),
('dump maker', 'dump a specific information(like shell command result, etc.); the command itself is congfigured in a task', 'free')
