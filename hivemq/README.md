
[官网](https://www.hivemq.com)

[开放MQTT服务](https://github.com/mqtt/mqtt.github.io/wiki/public_brokers)

## installer

- [jdk11](https://www.oracle.com/technetwork/java/javase/downloads/jdk11-downloads-5066655.html)

- [hivemq](https://www.hivemq.com/downloads/download-hivemq/)


## setup

- [hivemq env](https://github.com/qrsforever/opt/blob/master/hivemq/.env.sh)

- [jdk11 env](https://github.com/qrsforever/opt/blob/master/jdk/.env.sh)


## start service

- `export JAVA_OPTS="$JAVA_OPTS -Dhivemq.config.folder=${STOCKTECH_DIR}/hivemq/conf"`

- `xstart_hivemq`

- `netstat -an | grep 1883

## try out

- `http://localhost:8080 `

- username:`amdin` password:`hivemq`


## others

[默认配置](https://www.hivemq.com/docs/4.1/hivemq/configuration.html#default)

[连接报文](https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/)

