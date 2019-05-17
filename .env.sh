#!/bin/bash
#=================================================================
# date: 2019-05-09 21:39:06
# title: .env
#=================================================================

ENTER_DIR=`pwd`

export STOCKTECH_DIR=/system/source/stocktech

for file in `ls $STOCKTECH_DIR 2>/dev/null`
do
    path=$STOCKTECH_DIR/$file
    if [ -d $path -a -e $path/.env.sh ]
    then
        cd $path 2>/dev/null
        source .env.sh
        cd - 1>/dev/null
    fi
done

xrm_lessxk_files() {
    if [[ x$# != x2 ]]
    then
        echo "xrm_lessxk_files dir num"
        return
    fi
    echo "$ find $1 -size $2k -type f | xargs rm"
    echo -n "confirm(y/n): "
    read confirm
    if [[ x$confirm == xy ]]
    then
        find $1 -size $2k -type f | xargs rm
    fi
}

cd $ENTER_DIR
