## installer

[download](http://mosquitto.org/download/)

    sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
    sudo apt-get update

## compile source

    sudo apt-get install libc-ares-dev
    sudo apt-get install libc-ares2
    sudo apt-get install uuid-dev
    cd $MOSQUITTO_HOME
    make
    sudo make install

## configure

[官网](https://mosquitto.org/man/mosquitto-8.html#)

[密码配置](https://mosquitto.org/man/mosquitto_passwd-1.html)

    mosquitto_passwd [ -c | -D ] passwordfile username
    mosquitto_passwd -b passwordfile username password
    mosquitto_passwd -U passwordfile 

    mosquitto_passwd -b /etc/mosquitto/passwd stocktech stocktech


## start&stop

    netstat -an | grep "1883"
    sudo service mosquitto stop
    sudo service mosquitto start

    sudo mosquitto -c etc/mosquitto.conf -v
