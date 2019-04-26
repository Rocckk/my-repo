-- schema for creation of table `urls_to_sources`

create table `urls_to_sources` (
`source_id` int unsigned not null,

`url_id` int unsigned not null,

foreign key(`source_id`) references `sources`(`id`),

foreign key(`url_id`) references `urls`(`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;
