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
        logging.warn('on_close: '+self.name)
        if self.fsid in online_users:
            online_users.pop(self.fsid)
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
                    logging.warn('on_open: '+name)
                    send_msg2all(self.name, u'来了')
                    if fsid in online_users.keys():
                        online_users.pop(fsid)
                    send_comes(name)
                    online_users[fsid] = self
            elif self.fsid in online_users:
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

    from_fsid = Mgdb().get_fsid(from_name)
    to_fsid = Mgdb().get_fsid(to_name)

    if from_fsid in online_users:
        from_handler = online_users[from_fsid]
        if from_handler:
            from_handler.write_message(json.dumps(send))

    if to_fsid in online_users:
        to_handler = online_users[to_fsid]
        if to_handler:
            to_handler.write_message(json.dumps(send))


def send_comes(name):
    avatar = Mgdb().get_avatar(name)
    send = {'type': 2, 'from': name,
            'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}
    if avatar:
        send['msg'] = avatar
    for handler in online_users.values():
        handler.write_message(json.dumps(send))


def send_leaves(name):
    for handler in online_users.values():
        send = {'type': 3, 'from': name,
                'time': time.strftime('%H:%M:%S', time.localtime(time.time()))}
        handler.write_message(json.dumps(send))


class OnlineUsersHandler(BaseHandler):
    def get(self):
        names_avatars = []
        for handler in online_users.values():
            if handler.fsid != self.fsid:
                name_avatar = {}
                name_avatar['name'] = handler.name
                avatar = Mgdb().get_avatar(handler.name)
                if avatar:
                    name_avatar['avatar'] = avatar
                names_avatars.append(name_avatar)
        d = {'online_users': names_avatars}
        self.write_dict(d)


if __name__ == '__main__':
    c = None
    d = {"a": 1, "b": c}
    print d
