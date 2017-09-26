import src.Handlers as GameHandlers
import tornado.ioloop as ioloop
import tornado.web as web

from src.GamePool import GamePool
from src.lib.SequenceGenerator import Sequence


class Application(web.Application):
    def __init__(self):
        self.next_user_id = Sequence()
        self.game_pool = GamePool()

        settings = {
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "login_url": "/login",
            # TODO: true
            "xsrf_cookies": False,
        }

        handlers = (
            (r"/", GameHandlers.GameHandler),
            (r"/socket/", GameHandlers.GameSocket),
            # (r"/game/(.*)", game_handlers.GameHandler),
            # TODO: разобраться с кэшем, передавать параметром путь до статики(или отдельный конфиг)
            (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www/static/"}),
            (r"/test/(.*)", GameHandlers.TestHandler),
        )

        web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    application = Application()
    application.listen(8888)
    ioloop.IOLoop.instance().start()
