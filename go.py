#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time

import tornado
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler

import gvars
from handlers.chat import ChatHandler
from handlers.login import VerifyCodeHandler, RegisterHandler, LoginHandler


class MainHandler(RequestHandler):
    def get(self):
        self.render("templates/index.html")


class WeatherHandler(RequestHandler):
    def get(self):
        self.render("templates/weather.html")


class ChatroomHandler(RequestHandler):
    def get(self):
        fsid = self.get_cookie('fsid')
        if fsid:
            self.render("templates/chatroom.html")
        else:
            self.render("templates/register.html")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static")
}

application = tornado.web.Application(
    [
        (r"/", MainHandler),
        (r"/chat", ChatHandler),
        (r"/chatroom", ChatroomHandler),
        (r"/weather", WeatherHandler),
        (r"/verify_code", VerifyCodeHandler),
        (r"/register", RegisterHandler),
        (r"/login", LoginHandler)
    ], **settings
)

if __name__ == "__main__":
    # run on local
    port = 8000
    gvars.domain = '192.168.31.247'
    # run on server
    if len(sys.argv) == 2:
        port = sys.argv[1]
        gvars.domain = 'rome753.cc'
    application.listen(port)
    IOLoop.instance().start()
