#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import tornado
import tornado.websocket
import logging

import tuling
from handlers.base import BaseWebSocketHandler, BaseHandler
from mgdb import Mgdb
import copy

# name-BaseWebSocketHandler
online_users = {}


class ChatHandler(BaseWebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        pass

    def on_close(self):
        logging.warn('on_close')
        if self.name in online_users:
            online_users.pop(self.name)
        send_msg2all(self.name, u'走了')
        send_leaves(self.name)

    def on_message(self, message):
        msg = json.loads(message)

        if msg.has_key('type') and msg.has_key('to') and msg.has_key('msg'):
            # 验证发送过来的cookie
            if msg['type'] == 0:
                fsid = msg['msg'][:32]
                name = msg['msg'][32:]
                if Mgdb().find_login({'fsid': fsid, 'username': name}):
                    self.fsid = fsid
                    self.name = name
                    send_msg2all(self.name, u'来了')
                    if name in online_users.keys():
                        online_users.pop(name)
                    send_comes(name)
                    online_users[name] = self
            elif self.name in online_users:
                if msg['type'] == 1:# all
                    send_msg2all(self.name, msg['msg'])
                elif msg['type'] == 2: # name
                    send_msg2name(self.name, msg['to'], msg['msg'])
                elif msg['type'] == 3: # chat_robot
                    send_msg2name(self.name, msg['to'], msg['msg'])
                    text = tuling.tuling_chat(self.fsid, msg['msg'])
                    send_msg2name(msg['to'], self.name, text)


# 发送聊天室消息
def send_msg2all(from_name, msg):
    send = {'type': 0, 'from': from_name, 'msg': msg,
            'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}
    for handler in online_users.values():
        handler.write_message(json.dumps(send))


# 发送消息给某人
def send_msg2name(from_name, to_name, msg):
    send = {'type': 1, 'from': from_name, 'msg': msg,
            'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}

    if from_name in online_users:
        from_handler = online_users[from_name]
        if from_handler:
            from_handler.write_message(json.dumps(send))

    if to_name in online_users:
        to_handler = online_users[to_name]
        if to_handler:
            to_handler.write_message(json.dumps(send))


def send_comes(name):
    for handler in online_users.values():
        send = {'type': 2, 'from': name,
                'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}
        handler.write_message(json.dumps(send))


def send_leaves(name):
    for handler in online_users.values():
        send = {'type': 3, 'from': name,
                'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}
        handler.write_message(json.dumps(send))


class OnlineUsersHandler(BaseHandler):
    def get(self):
        names = online_users.keys()
        if self.name in names:
            names.remove(self.name)
        d = {'online_users': names}
        self.write_dict(d)


if __name__ == '__main__':
    d = {"a": 1, "b": 2}
    k = d.keys()
    k.remove("c")
    print k
    print d.keys()
