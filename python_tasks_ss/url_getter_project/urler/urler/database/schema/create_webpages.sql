-- this is the script for creation of table `webpages`

create table `webpages`(

`id` int unsigned not null auto_increment primary key,

`url` varchar(200),

`time_crawled` datetime,

`crawl_count` int unsigned not null

)

engine InnoDB

default charset utf8


