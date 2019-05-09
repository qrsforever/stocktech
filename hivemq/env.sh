#!/bin/bash
#=================================================================
# date: 2019-05-10 00:06:01
# title: env
#=================================================================

export HIVEMQ_PORT=1883
export JAVA_OPTS="$JAVA_OPTS -Dhivemq.config.folder=${STOCKTECH_DIR}/hivemq/conf"
export JAVA_OPTS="$JAVA_OPTS -Dhivemq.extensions.folder=${STOCKTECH_DIR}/hivemq/extensions"

alias xstart_hivemq='$HIVEMQ_HOME/bin/run.sh'
