#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @file send.py
# @brief
# @author QRS
# @home qrsforever.github.io
# @version 1.0
# @date 2019-05-09 16:58:28

import os
import smtplib
from email.mime.text import MIMEText

g_mail_host = 'smtp.qq.com'
g_mail_user = os.environ.get('U1')
g_mail_pass = os.environ.get('E1')

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
