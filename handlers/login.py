#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys
import uuid
from uuid import uuid4

import json

from tornado.web import HTTPError

import gvars
import sys_email
from handlers.base import BaseHandler
from mgdb import Mgdb
import urllib2
import logging

# emails and verify codes
emails_codes = {}

name = u'username'
word = u'password'
mail = u'email'


class VerifyCodeHandler(BaseHandler):
    def post(self):
        email = json.loads(self.request.body.decode('utf-8'))

        if Mgdb().find_email(email):
            logging.debug('email already exist')
        else:
            v_code = sys_email.send_verify_code(email[mail])
            if v_code is not None:
                emails_codes[email[mail]] = v_code
            else:
                logging.debug('send email failed')


class RegisterHandler(BaseHandler):

    def post(self):
        register = json.loads(self.request.body.decode('utf-8'))

        if check_register(register) is True:
            if Mgdb().add_register(register) is True:
                self.write({"error_code": 200, "reason": "注册成功"})
            else:
                self.write({"error_code": 200, "reason": "用户名或邮箱已存在"})

        else:
            self.write({"error_code": 200, "reason": "信息填写有误"})

        # if register['verify_code'] == emails_codes[register['email']]:
        #     pass


def validate_email(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",
                    email) is not None:
            return True


def check_register(r):
    if r.has_key(name) and r.has_key(word) and r.has_key(mail):
        if r[name].strip() != '' and r[word].strip() != '' and validate_email(r[mail]) is True:
            return True


class LoginHandler(BaseHandler):

    def post(self):
        user = json.loads(self.request.body.decode('utf-8'))

        logging.debug(self.get_cookie('fsid'))
        if Mgdb().is_exists(user):
            logging.debug('login success')
            fsname = user[name]
            fsid = Mgdb().get_fsid(fsname)
            self.set_cookie('fsid', fsid, gvars.domain, expires_days=30)
            self.set_cookie('fsname', fsname, gvars.domain, expires_days=30)

            self.write({"error_code": 200, "reason": "登录成功"})
        else:
            logging.debug('login fail')
            self.write({"error_code": 3, "reason": "login fail"})


if __name__ == "__main__":
    # run on local
    pass
    r = {u'username': u'\u8d85\u54e5', u'password': u'chao'}
    logging.debug(Mgdb().is_exists(r))