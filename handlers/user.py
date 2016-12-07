#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import tornado
import logging
import os
import uuid

from bson import ObjectId

import gvars
from handlers.base import BaseHandler
from mgdb import Mgdb


class UserHandler(BaseHandler):

    def get(self):
        name = self.get_argument('name')
        user = Mgdb().find_user({'name': name})
        if user:
            if 'avatar' in user:
                user['avatar'] = gvars.image_url + user['avatar']
            self.write_dict(user)
        else:
            self.write_base('用户不存在')

    def post(self):
        if Mgdb().update_user(self.name, self.jsonbody):
            self.write_base('更新成功')
        else:
            self.write_base('更新失败')


class AvatarHandler(BaseHandler):

    def post(self):
        files = self.request.files.get('file')
        if files:
            avatar = files[0]
            ext = os.path.splitext(avatar['filename'])[1]
            filename = str(time.time()) + ext
            avatar_file = get_image_file(filename)

            with open(avatar_file, 'wb') as f:
                f.write(avatar['body'])
                logging.warn('upload: ' + avatar_file)

                Mgdb().update_avatar(self.name, filename)
                self.write_base("上传成功")


def get_image_file(filename):
    image_file = os.path.join(gvars.image_dir, filename)
    return image_file


if __name__ == '__main__':

    u1 = uuid.uuid1()
    u4 = uuid.uuid4()
