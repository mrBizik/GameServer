import json

import tornado.web
import tornado.ioloop

import GameSocket

from GamePool import GamePool

from lib.SequenceGenerator import Sequence


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie("user_id", self.get_argument("user_id"))
        self.render('templates/index.html')

class Application(tornado.web.Application):
    def __init__(self):
        self.next_user_id = Sequence()
        self.game_pool = GamePool()

        settings = {
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            # "login_url": "/login",
            # "xsrf_cookies": True,
        }

        handlers = (
            (r'/', MainHandler),
            (r'/game/(.*)', GameSocket.GameSocket),
            # TODO: разобраться с кэшированием, возможно отдавать статику ч-з nginx
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        )

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    application = Application()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()