# coding=utf-8
import logging
import traceback
import json
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler


class BaseHandler(RequestHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.fsid = self.get_cookie('fsid')
        self.name = self.get_cookie('fsname')
        if self.request.body:
            self.jsonbody = json.loads(self.request.body.decode('utf-8'))

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish('{code: ' + str(status_code) + ', message: ' + self._reason + '}')

    def write_base(self, reason='OK', error_code=200):
        self.write_dict({'reason': reason})

    def write_dict(self, d):
        if '_id' in d:
            d.pop('_id')
        d['error_code'] = 200
        if 'reason' not in d:
            d['reason'] = 'OK'
        self.write(d)


class BaseWebSocketHandler(WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(BaseWebSocketHandler, self).__init__(application, request, **kwargs)
        self.fsid = ""
        self.name = ""


def convert_to_builtin_type(obj):
    d = {}
    d.update(obj.__dict__)
    return d


class BaseResponse(object):

    def __init__(self, error_code=200, reason='OK'):
        self.error_code = error_code
        self.reason = reason

    def to_json(self):
        return json.dumps(self, default=convert_to_builtin_type)


class User(BaseResponse):

    def __init__(self, age, city, quote):
        BaseResponse.__init__(self)
        self.age = age
        self.city = city
        self.quote = quote


if __name__ == "__main__":
    import json
    j = '{"age": 23, "name": "\u6253\u53d1\u65af\u8482\u82ac"}'
    d = json.loads(j)
    print d['name']
