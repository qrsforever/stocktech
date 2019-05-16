#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file send.py
# @brief
# @author QRS
# @blog qrsforever.github.io
# @version 1.0
# @date 2019-05-09 16:58:28

import os
import smtplib
from email.mime.text import MIMEText
import paho.mqtt.client as mqtt

g_mail_host = 'smtp.qq.com'
g_mail_user = os.environ.get('U1')
g_mail_pass = os.environ.get('E1')

g_mqtt_host = os.environ.get('HOST', '127.0.0.1')
g_mqtt_user = os.environ.get('MQTT_U', 'stocktech')
g_mqtt_pass = os.environ.get('MQTT_P', 'stocktech')
g_mqtt_clii = os.environ.get('MQTT_C', 'crawl0001')

def send_mail(txt, subtype='plain', sender='985612771@qq.com',
        receivers=['705723886@qq.com', '714871911@qq.com']):
    msg = MIMEText(txt, subtype, 'utf-8')
    msg['From'] = sender
    msg['To'] = receivers[0]
    msg['Subject'] = 'stocktech reminder'
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(g_mail_host, 25)
        smtpObj.login(g_mail_user, g_mail_pass)
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)

def send_mqtt(topic, txt, timeout=1):
    client = mqtt.Client(g_mqtt_clii)
    client.username_pw_set(g_mqtt_user, g_mqtt_pass);

    def _on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.publish(topic, txt, qos=0)
            client.disconnect()
    client.on_connect = _on_connect
    client.connect(g_mqtt_host, 1883, 60)
    client.loop(timeout) # for connack
    client.loop(timeout) # for puback
    client.loop(0.2) # wait 0.2
