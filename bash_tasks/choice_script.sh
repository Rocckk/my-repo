#!/usr/local/bin/bash

echo "what exactly he wants to check?"
echo "1. Number of CPU Cores"
echo "2. Disk space"
echo "3. Size of RAM"
echo "4. who are the last users which were logged in on the host"
echo "5. calculate the number of active python/perl processes"

read input;

case $input in
    1) echo "you seleected Number of CPU Cores"
        echo "the number of cpu cores iв $(sysctl -n hw.ncpu)"
        ;;
    2) echo "you seleected Disk space"
        echo "the total space on your computer is $(df -h | tr -s ' ' | sed -e '3,$ d' -e '1 d'| cut -d ' ' -f 2)"
        echo "the used space is $(df -h | tr -s ' ' | sed -e '3,$ d' -e '1 d'| cut -d ' ' -f 3)"
        echo "the available space is $(df -h | tr -s ' ' | sed -e '3,$ d' -e '1 d'| cut -d ' ' -f 4)"
        ;;
    3) echo "you seleected Size of RAM"
        size=$(sysctl -n hw.physmem)
        echo $size
        echo "The size of your RAM is $(echo "scale=1; $size  / 1000000000" | bc) gigabytes"
        ;;
    4) echo -e "you seleected the last users which were logged in on the host\n"
        echo -e "the last 5 users who were logged in on the host are:\n"
        last | tr -s '  ' | awk 'length($0) > 30' | head -5
        ;;
    5) echo -e "you seleected to calculate the number of active python/perl processes\n"
        echo "the number of python processes is $(ps -A | grep 'python' | grep -cv 'grep')"
        echo "the number of perl processes is $(ps -A | grep 'perl' | grep -cv 'grep')"
        ;;
    *) echo 'no choice was provided or the script got run by a cron, not human )'
esac
