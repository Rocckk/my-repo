#! /usr/local/bin/bash

#this solution assumes that the input log file is standard and IPs are all located at a certain place in a line (as in the tested Apache  access.log file)!

PATTERN="([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"



echo -e "Unique IPs, got with egrep, sorted in ascending order are:\n
$(egrep -wo $PATTERN $1 | sort -n  -t .  -k 1,1 -k 2,2 -k 3,3 -k 4,4  | uniq -c )"

echo "Unique IPs, got with awk, sorted in ascending order are:"
awk -v pattern=$PATTERN '$0 ~ pattern' $1 | sort -n  -t .  -k 1,1 -k 2,2 -k 3,3 -k 4,4 | cut -d - -f 1 | uniq -c
