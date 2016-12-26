#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
import time
import tornado
import tornado.websocket
import logging

import gvars
import tuling
from handlers.base import BaseWebSocketHandler, BaseHandler
from mgdb import Mgdb
import copy

# name-BaseWebSocketHandler
online_users = {}

ROBOTS = ['lara', ]


class ChatHandler(BaseWebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        pass

    def on_close(self):
        if self.fsid in online_users and self == online_users[self.fsid]:
            logging.warn('on_close: '+ self.name)
            online_users.pop(self.fsid)
            send_leaves(self.name)

    def on_message(self, message):
        if isinstance(message, unicode): # 普通消息
            msg = json.loads(message)
            if msg.has_key('type') and msg.has_key('to') and msg.has_key('msg'):
                # 验证发送过来的cookie
                if msg['type'] == 99:
                    fsid = msg['msg'][:32]
                    name = msg['msg'][32:]
                    if Mgdb().find_user({'fsid': fsid, 'name': name}):
                        self.fsid = fsid
                        self.name = name
                        logging.warn('on_open: '+ str(id(self)))
                        send_comes(name)
                        # 移除同一用户旧的handler
                        if fsid in online_users.keys():
                            online_users.pop(fsid)
                        send_comes(name)
                        online_users[fsid] = self

                elif self.fsid in online_users:
                    # image:// + 图片url
                    if msg['msg'] == 'image://' and self.temp:
                        msg['msg'] += gvars.image_url + self.temp
                        self.temp = None
                    if msg['type'] == 0:# all
                        send_msg2all(self.name, msg['msg'])
                    elif msg['type'] == 1: # name
                        if msg['to'] in ROBOTS: # robot
                            send_msg2name(self.name, msg['to'], msg['msg'])
                            text = tuling.tuling_chat(self.fsid, msg['msg'])
                            send_msg2name(msg['to'], self.name, text)
                        else: # person
                            send_msg2name(self.name, msg['to'], msg['msg'])
        else: # 二进制文件, 先缓存到 self.temp, 接收到下一条文本消息再处理
            self.temp = str(time.time())+'.jpg'
            temp = os.path.join(gvars.image_dir, self.temp)
            with open(temp, 'wb') as f:
                f.write(message)



# 发送聊天室消息
def send_msg2all(from_name, msg):
    send = {'type': 0, 'from': from_name, 'msg': msg,
            'time': get_time()}
    for handler in online_users.values():
        if handler:
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
        if handler:
            handler.write_message(json.dumps(send))


def send_leaves(name):
    for handler in online_users.values():
        if handler:
            send = {'type': 3, 'from': name,
                    'time': get_time()}
            handler.write_message(json.dumps(send))


def get_time():
    return long(time.time())


def add_robot():
    for robot in ROBOTS:
        online_users[robot] = False


class OnlineUsersHandler(BaseHandler):
    def get(self):
        names_avatars = []
        for fsid in online_users.keys():
            if fsid != self.fsid:
                if fsid in ROBOTS:
                    name = fsid
                    avatar = Mgdb().get_avatar(name)
                    if not avatar:
                        avatar = ''
                else:
                    user = Mgdb().find_user({"fsid": fsid})
                    name = user['name']
                    if 'avatar' in user:
                        avatar = gvars.image_url + user['avatar']
                    else:
                        avatar = ''
                names_avatars.append({'name': name, 'avatar': avatar})
        d = {'online_users': names_avatars}
        self.write_dict(d)


if __name__ == '__main__':
    c = False
    d = {"a": 1, "b": c}
    if c:
        print 'true'
    else:
        print 'false'

