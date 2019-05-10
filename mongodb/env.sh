#!/bin/bash
#=================================================================
# date: 2019-05-10 00:06:01
# title: env
#=================================================================

stocktech_mongod_dir=`dirname ${BASH_SOURCE[0]}`
stocktech_mongod_dir=`cd ${stocktech_mongod_dir}; pwd`

alias xstart_mongod='mongod -f $stocktech_mongod_dir/conf/mongod.conf'
