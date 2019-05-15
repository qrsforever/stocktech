#!/bin/bash
#=================================================================
# date: 2019-05-15 13:18:00
# title: env
#=================================================================

stocktech_mosquitto_dir=`dirname ${BASH_SOURCE[0]}`
stocktech_mosquitto_dir=`cd ${stocktech_mosquitto_dir}; pwd`

xstart_mosquitto() {
    sudo service mosquitto stop
    mosquitto -c $stocktech_mosquitto_dir/etc/mosquitto.conf -v -p 1883
}
