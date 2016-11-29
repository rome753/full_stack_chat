#!/usr/bin/env python
# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
import random
import smtplib
import logging

import gvars

mail_host = 'smtp.163.com'
mail_user = 'fullstacks'
mail_pass = 'xxxxxx'
mail_postfix = '163.com'


def send_mail(to_list, sub, content):
    me = 'hello' + '<' + mail_user + '@' + mail_postfix + '>'
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        logging.warn(str(e))
        return False


def send_verify_code(mailto):
    v_code = str(random.randint(1000, 9999))
    if send_mail([mailto, ], 'dear tom: good night', 'hi,<br/>' + v_code):
        return v_code


if __name__ == '__main__':
    send_verify_code("rome753@163.com")
