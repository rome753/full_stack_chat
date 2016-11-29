import traceback
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler


class BaseHandler(RequestHandler):

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish('{code: ' + str(status_code) + ', message: ' + self._reason + '}')


class BaseWebSocketHandler(WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.fsid = ""
        self.name = ""
        self.ws_connection = None
        self.close_code = None
        self.close_reason = None
        self.stream = None
        self._on_close_called = False
