#!/bin/bash
#=================================================================
# date: 2019-05-15 13:17:47
# title: env
#=================================================================

stocktech_reminder_dir=`dirname ${BASH_SOURCE[0]}`
stocktech_reminder_dir=`cd ${stocktech_reminder_dir}; pwd`

for file in `ls $stocktech_reminder_dir 2>/dev/null`
do
    path=$stocktech_reminder_dir/$file
    if [ -d $path -a -e $path/.env.sh ]
    then
        cd $path 2>/dev/null
        source .env.sh
        cd - 1>/dev/null
    fi
done
