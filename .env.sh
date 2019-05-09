#!/bin/bash
#=================================================================
# date: 2019-05-09 21:39:06
# title: .env
#=================================================================


export STOCKTECH_DIR=/system/source/stocktech


# hivemq
export HIVEMQ_PORT=1883
export JAVA_OPTS="$JAVA_OPTS -Dhivemq.config.folder=${STOCKTECH_DIR}/hivemq/conf"
