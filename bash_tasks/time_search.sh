#!/usr/local/bin/bash

PATTERN="([0-1][0-9]|[2][0-4]):[0-5][0-9]:[0-5][0-9]"
 echo "$ is $1"
echo "the time in format hh:mm:ss is:"
egrep -wo $PATTERN  $1
