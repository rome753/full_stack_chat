#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import time
import tornado
import logging
import os
import uuid

import gvars
from handlers.base import BaseHandler
from mgdb import Mgdb


class AvatarHandler(BaseHandler):

    def get(self):
        pass

    def post(self):
        files = self.request.files.get('file')
        if files:
            avatar = files[0]
            ext = os.path.splitext(avatar['filename'])[1]
            name = str(time.time())
            avatar_file = get_image_file(name + ext)

            with open(avatar_file, 'wb') as f:
                f.write(avatar['body'])
                logging.warn('upload: ' + avatar_file)
                self.write({"error_code": 200, "reason": "上传成功"})


def get_image_file(filename):
    image_file = os.path.join(gvars.image_dir, filename)
    return image_file


if __name__ == '__main__':

    u1 = uuid.uuid1()
    u4 = uuid.uuid4()
    a =  time.time()
    print __file__
