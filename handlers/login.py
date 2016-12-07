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
    '''
    注册
    '''

    def post(self):
        if check_register(self.jsonbody) is True:
            if Mgdb().add_login(self.jsonbody) is True:
                self.write_base("注册成功")
            else:
                self.write_base("用户名或邮箱已存在")

        else:
            self.write_base("信息填写有误")

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
    '''
    登录
    '''

    def post(self):
        logging.debug(self.fsid)
        if Mgdb().find_login(self.jsonbody):
            logging.debug('登录成功')
            fsname = self.jsonbody[name]
            fsid = Mgdb().get_fsid(fsname)
            self.set_cookie('fsid', fsid, gvars.domain, expires_days=30)
            self.set_cookie('fsname', fsname, gvars.domain, expires_days=30)

            self.write_base("登录成功")
        else:
            logging.debug('登录失败')
            self.write_base("登录失败")


class LogoutHandler(BaseHandler):
    '''
    退出登录
    '''

    def get(self):
        self.write_base("退出登录成功")
        if self.name:
            logging.warn('logout: '+self.name)


if __name__ == "__main__":
    # run on local
    pass
    r = {u'username': u'\u8d85\u54e5', u'password': u'chao'}
    logging.debug(Mgdb().find_login(r))