#!/bin/bash
#=================================================================
# date: 2019-05-15 13:18:00
# title: env
#=================================================================

stocktech_mosquitto_dir=`pwd`

xstart_mosquitto() {
    sudo service mosquitto stop
    sleep 1
    mosquitto -c $stocktech_mosquitto_dir/etc/mosquitto.conf -v
}
