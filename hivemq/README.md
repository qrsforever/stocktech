
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

- `export JAVA_OPTS="$JAVA_OPTS -Dhivemq.extensions.folder=$${STOCKTECH_DIR}/hivemq/extensions"`

- `service mosquitto stop` because it bind 1883 if exist

- `xstart_hivemq`

- `netstat -pan | grep 1883

## try out

- `http://localhost:8080 `

- username:`amdin` password:`hivemq`

## extensions

[sdk sample](https://github.com/hivemq/hivemq-extension-sdk)

### mvn dependecy

- [mongod driver](https://github.com/mongodb/mongo-java-driver)

- [dom4j](https://dom4j.github.io/)

[dom4j FAQ](https://github.com/dom4j/dom4j/wiki/FAQ)
 
**[错误](https://my.oschina.net/u/2438514/blog/534450#comments)**

**JAVA XML Parse太辣鸡, 改用mongodb**

### mvn generate stocktech extension

    mvn archetype:generate \
        -DarchetypeGroupId=com.hivemq \
        -DarchetypeArtifactId=hivemq-extension-archetype \
        -DarchetypeVersion=4.0.0 \
        -DgroupId=com.hivemq.extensions \
        -DartifactId=stocktech-extension \
        -Dversion=1.0.0 \
        -Dpackage=com.hivemq.extensions.stocktech \
        -DinteractiveMode=false

### mvn clean

### mvn package

### deploying stocktech-extension

    unzip src/stocktech-extension/target/stocktech-extension-1.0.0-distribution.zip -d extensions


## others

[默认配置](https://www.hivemq.com/docs/4.1/hivemq/configuration.html#default)

[连接报文](https://www.hivemq.com/blog/mqtt-essentials-part-3-client-broker-connection-establishment/)

[extensions介绍](https://www.hivemq.com/docs/4/extensions/introduction.html)
