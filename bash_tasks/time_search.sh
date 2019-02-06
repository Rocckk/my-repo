#!/usr/local/bin/bash
 echo "$ is $1"
echo "the current time in format hh:mm:ss is:"
egrep -wo "([0-1][0-9]|[2][0-4]):[0-5][0-9]:[0-5][0-9]" $1
