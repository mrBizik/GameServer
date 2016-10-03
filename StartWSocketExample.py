import json

import tornado.web
import tornado.ioloop

import GameSocket

from GamePool import GamePool

from lib.SequenceGenerator import Sequence

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')


class Application(tornado.web.Application):
    def __init__(self):
        self.next_user_id = Sequence()
        self.game_pool = GamePool()

        handlers = (
            (r'/', MainHandler),
            (r'/game/(.*)', GameSocket.GameSocket),
            # TODO: разобраться с кэшированием, возможно отдавать статику ч-з nginx
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        )

        # TODO: заменить на super?
        tornado.web.Application.__init__(self, handlers)

application = Application()


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()