import json

import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.gen as gen

from tornado import template

import time

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#          self.render('index.html', messages=None)


class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        self.ws_connection.write_message("Hello!")

    def on_message(self, message):
       self.ws_connection.write_message(message)
       self.sleep_my_baby()

    def on_close(self, message=None):
        self.ws_connection.write_message("Bye!")

    def check_origin(self, origin):
        return True

    # @tornado.web.asynchronous
    @gen.coroutine
    def sleep_my_baby(self):
       yield time.sleep(30)
       print('Oh shit, i am sleeping!')
       self.ws_connection.write_message('Graaaaa!')


class Application(tornado.web.Application):
    def __init__(self):
        self.webSocketsPool = []

        # settings = {
        #     'static_url_prefix': '/static/',
        # }
        handlers = (
            (r'/', WebSocket),
            # (r'/websocket/?', WebSocket),
            # (r'/static/(.*)', tornado.web.StaticFileHandler,
            #  {'path': 'static/'}),
        )

        tornado.web.Application.__init__(self, handlers)

application = Application()


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()