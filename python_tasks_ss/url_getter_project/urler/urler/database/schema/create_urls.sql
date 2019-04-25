-- this is the script for creation of table `scraped_urls`

create table `scraped_urls`(

`webpage_id` int unsigned not null,

`url` varchar(200),

`count_on_page` int unsigned not null,

foreign key(`webpage_id`) references `webpages`(`id`)

)

engine InnoDB

default charset utf8
