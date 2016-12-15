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
        if self.fsid in online_users and self == online_users[self.fsid]:
            logging.warn('on_close: '+ self.name)
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
                    logging.warn('on_open: '+ str(id(self)))
                    send_msg2all(self.name, u'来了')
                    # 移除同一用户旧的handler
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
            'time': get_time()}
    for handler in online_users.values():
        handler.write_message(json.dumps(send))


# 发送消息给某人
def send_msg2name(from_name, to_name, msg):
    """
    A发送给B一条消息, 系统要给A和B各发一条
    A收到{type: -1, from: B}
    B收到{type: 1, from: A}
    """
    send = {'msg': msg, 'time': get_time()}

    from_fsid = Mgdb().get_fsid(from_name)
    to_fsid = Mgdb().get_fsid(to_name)

    if from_fsid in online_users:
        from_handler = online_users[from_fsid]
        if from_handler:
            send['type'] = -1
            send['from'] = to_name
            from_handler.write_message(json.dumps(send))

    if to_fsid in online_users:
        to_handler = online_users[to_fsid]
        if to_handler:
            send['type'] = 1
            send['from'] = from_name
            to_handler.write_message(json.dumps(send))


def send_comes(name):
    avatar = Mgdb().get_avatar(name)
    send = {'type': 2, 'from': name,
            'time': get_time()}
    if avatar:
        send['msg'] = avatar
    for handler in online_users.values():
        handler.write_message(json.dumps(send))


def send_leaves(name):
    for handler in online_users.values():
        send = {'type': 3, 'from': name,
                'time': get_time()}
        handler.write_message(json.dumps(send))


def get_time():
    return long(time.time())


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
    print get_time()
