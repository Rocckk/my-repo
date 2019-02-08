 #!/usr/local/bin/bash

PATTERN="([^[:punct:]]|^)\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b([^[:punct:]]|$)"

#awk on FreeBSD has some differences in regex operators: no word boundaries match, but as we iterate through the record (line) with a loop, operators ^ and $ can be used instead to separate valid Ips from other context; the literal dot(.) must be escaped twice with backslashes 
PATTERN_AWK='^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$'

echo "ipv4 addresses will be checked now using egrep!"

echo -e "this is optimal solution:\nthe results are valid IPS, the ambiguous results (sequences of numbers, numbers and letters are excluded; \nmatches separated from other characters with any punctuation marks are excluded to provide a clearer result)"

egrep -o $PATTERN $1 | tr -d ' '

echo "ipv4 addresses will be checked now using awk with loop!"

awk -v pattern=$PATTERN_AWK '{for (i=1; i<=NF; i++){
                                 if ($i ~ pattern){
                                    print $i;
                                }
                              }
                             }' $1
