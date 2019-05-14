#!/bin/bash

# this is the script for creating statements to populate the db with the initial data
name="Client"
group_name="Group"
descr="Some description"
for num in {1..50}
do
   echo "insert into \`api_synergy_groups\` (\`id\` ,\`name\`, \`description\`) values ('$num', '$group_name$num', '$descr $num');" >> ./data/insert_groups.sql
   echo "insert into \`api_synergy_users\` (\`id\`, \`username\`, \`created\`, \`group_id_id\`) values ('$num', '$name$num', now(), '$num');" >> ./data/insert_users.sql

done
