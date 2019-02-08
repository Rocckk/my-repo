#!/usr/local/bin/bash

PATTERN='[0-9]{1,4}'
if [ $1 ]; then
    # here we direct stdout and stderr to the data sink to suppress standard behavior of the commmand
    if ps -U $1 &> /dev/null; then
        echo "the PIDs of the processes run by user $1 are:"
        ps -U $1 | sed '1 d' | cut -c '1-5'
        echo "same task preformed with awk:"
        ps -U $1 | sed '1 d' | awk '{print $1}'
    else
        echo "There are npo processes run by this user!"
    fi
else
    echo "the PIDs of the processes run by user $(whoami) are:"
    ps -U $(whoami) | sed '1 d' | cut -c '1-5'
    echo "same task preformed with awk:"
    ps -U $(whoami) | sed '1 d' | awk '{print $1}'
fi                                                            
