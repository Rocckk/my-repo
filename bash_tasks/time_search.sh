#!/usr/local/bin/bash

PATTERN="([0-1][0-9]|[2][0-4]):[0-5][0-9]:[0-5][0-9]"
AWK_PATTERN="([0-1][0-9]|[2][0-4]):[0-5][0-9]:[0-5][0-9]$"
 echo "$ is $1"
echo "the time in format hh:mm:ss, found by egrep is:"
egrep -wo $PATTERN  $1

echo "the same time found with awk:"

# as there is no way to show only the matching part of a field in awk, below we use standard variables RSTART and RLENGTH to display only the matching subsctrings 
awk -v pattern=$AWK_PATTERN '
                            {for (i=1; i<=NF; i++){
                                m=match($i, pattern)
                                if ($i ~ pattern){
                                    print substr ($i,RSTART, RSTART + RLENGTH)
                                }
                            }
                            }' $1
