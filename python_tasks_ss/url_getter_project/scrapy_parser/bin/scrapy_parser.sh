#!/usr/local/bin/bash

export PYTHONPATH="/usr/home/itymos/git_thing/my-repo/python_tasks_ss/url_getter                                                                                                                                                             _project/scrapy_parser/src"

if [ $1 ]; then
    cd ../etc/
    current_location=$(pwd)
    if [[ $current_location = */etc ]]; then
        scrapy crawl x_spider -a url=$1
    else
        echo "incorrect location for the script execution! please run the script
from inside the project's /bin folder"
    fi
else
    echo "The source URL was not provided to the script!"
fi

