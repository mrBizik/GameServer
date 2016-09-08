import json

import tornado.web
import tornado.ioloop

import GameSocket

from lib.SequenceGenerator import Sequence

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')


class Application(tornado.web.Application):
    def __init__(self):
        self.next_user_id = Sequence()
        # TODO: Запилить контроллер
        self.game_controller = None

        handlers = (
            (r'/', MainHandler),
            (r'/game/(.*)', GameSocket.GameSocket),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        )

        tornado.web.Application.__init__(self, handlers)

application = Application()


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()