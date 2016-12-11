#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time

import tornado
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler

import gvars
from handlers import handlers

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

HANDLERS = [
        (r"/", MainHandler),
        (r"/chatroom", ChatroomHandler),
        (r"/weather", WeatherHandler),
]

if __name__ == "__main__":
    # run on local
    gvars.port = 8000
    gvars.domain = '192.168.31.247'
    # gvars.domain = '192.168.1.28'
    gvars.image_dir = './static/upload/image'
    # run on server
    if len(sys.argv) == 2:
        gvars.port = sys.argv[1]
        gvars.domain = 'rome753.cc'
        # 服务器上用Supervisor运行时, 使用绝对路径
        gvars.image_dir = '/root/full_stack/static/upload/image'

    gvars.image_url = "http://" + gvars.domain + ":" + str(gvars.port)+"/static/upload/image/"

    HANDLERS += handlers
    application = tornado.web.Application(HANDLERS, **settings)
    application.listen(gvars.port)
    IOLoop.instance().start()
