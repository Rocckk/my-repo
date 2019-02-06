#!/usr/local/bin/bash

echo "ipv4 addresses will be checked now!"



echo -e "this is optimal solution:\nthe results are valid IPS, the ambiguous results (sequences of numbers, numbers and letters are excluded; \nmatches separated from other characters with any punctuation marks are excluded to provide a clearer result)"

egrep -o  "([^[:punct:]]|^)\b([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\b([^[:punct:]]|$)" $1 | tr -d ' '
