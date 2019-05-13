#!/bin/bash
#=================================================================
# date: 2019-05-10 00:06:01
# title: env
#=================================================================

stocktech_hivemq_dir=`dirname ${BASH_SOURCE[0]}`
stocktech_hivemq_dir=`cd ${stocktech_hivemq_dir}; pwd`

export HIVEMQ_PORT=1883
export JAVA_OPTS="$JAVA_OPTS -Dhivemq.config.folder=${stocktech_hivemq_dir}/conf"
export JAVA_OPTS="$JAVA_OPTS -Dhivemq.extensions.folder=${stocktech_hivemq_dir}/extensions"

# sudo service mosquitto stop

alias xstart_hivemq='$HIVEMQ_HOME/bin/run.sh'

xdeploy_stocktech_extension() {
    n="stocktech-extension"
    echo "${stocktech_hivemq_dir}/extensions/$n"
    if [[ -d ${stocktech_hivemq_dir}/extensions/$n ]]
    then
        touch ${stocktech_hivemq_dir}/extensions/$n/DISABLED
        sleep 3
        rm -rf ${stocktech_hivemq_dir}/extensions/$n/*
    fi
    unzip ${stocktech_hivemq_dir}/src/$n/target/$n-*.zip -d ${stocktech_hivemq_dir}/extensions
    sleep 2
    if [[ -f ${stocktech_hivemq_dir}/extensions/$n/DISABLED ]]
    then
        rm -rf ${stocktech_hivemq_dir}/extensions/$n/DISABLED
    fi
}
