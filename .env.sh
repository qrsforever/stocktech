#!/bin/bash
#=================================================================
# date: 2019-05-09 21:39:06
# title: .env
#=================================================================


export STOCKTECH_DIR=/system/source/stocktech

for file in `ls $STOCKTECH_DIR 2>/dev/null`
do
    path=$STOCKTECH_DIR/$file
    if [ -d $path -a -e $path/env.sh ]
    then
        cd $path 2>/dev/null
        source env.sh
        cd - 1>/dev/null
    fi
done
