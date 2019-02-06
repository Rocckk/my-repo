#!/usr/local/bin/bash

echo "the PIDs of the processes run by user $(whoami) are:"

ps -U itymos | sed '1 d' | cut -c '1-5'
