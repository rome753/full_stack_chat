#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import tornado
import tornado.websocket
import logging

from handlers.base import BaseWebSocketHandler
from mgdb import Mgdb

online_users = []

class ChatHandler(BaseWebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        pass

    def on_close(self):
        if self in online_users:
            online_users.remove(self)
        send_msg2all(self, u'走了')

    def on_message(self, message):
        msg = json.loads(message)

        if msg.has_key('type') and msg.has_key('to') and msg.has_key('msg'):
            # 验证发送过来的cookie
            if msg['type'] == 0:
                fsid = msg['msg'][:32]
                name = msg['msg'][32:]
                logging.debug(fsid + ":" + name)
                if Mgdb().find_login({'fsid': fsid, 'username': name}):
                    self.fsid = fsid
                    self.name = name
                    if self not in online_users:
                        online_users.append(self)
                        send_msg2all(self, u'来了')
            elif self in online_users:
                if msg['type'] == 1:
                    send_msg2all(self, msg['msg'])


def send_msg2all(handler, msg):
    send = {}
    send['type'] = 0
    send['from'] = handler.name
    send['msg'] = msg
    send['time'] = time.strftime('(%H:%M:%S): ', time.localtime(time.time()))
    logging.debug(send)
    for user in online_users:
        user.write_message(json.dumps(send))
