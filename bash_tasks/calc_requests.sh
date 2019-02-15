#!/usr/local/bin/bash

if [ $1 ]; then
    echo "The number of requests to the IP $1 in the file access.log.1 located in my home directory is"
    # the parameter should be taken out and dots should be escaped to provide proper match!!
    ip_with_escapes=$(echo $1 | sed s/'\.'/'\\.'/g)
    egrep -wo "$ip_with_escapes" $HOME/access.log.1 | uniq -c
else
    egrep -wo "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])" $HOME/access.log.1 | uniq -c | less
fi
