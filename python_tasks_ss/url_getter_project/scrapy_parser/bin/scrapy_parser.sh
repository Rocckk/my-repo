#!/usr/local/bin/bash

export PYTHONPATH="/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_getter_project/scrapy_parser/src"

scrapy crawl x_spider -a url=$1
