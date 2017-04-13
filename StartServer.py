import tornado.web as web
import tornado.ioloop as ioloop

import Handlers as game_handlers
from GamePool import GamePool

from lib.SequenceGenerator import Sequence


class Application(web.Application):
    def __init__(self):
        self.next_user_id = Sequence()
        self.game_pool = GamePool()

        settings = {
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            # "login_url": "/login",
            # "xsrf_cookies": True,
        }

        handlers = (
            (r"/", game_handlers.GameHandler),
            (r"/socket/(.*)", game_handlers.GameSocket),
            # (r"/game/(.*)", game_handlers.GameHandler),
            # TODO: разобраться с кэшированием, возможно отдавать статику ч-з nginx
            (r"/static/(.*)", web.StaticFileHandler, {"path": "static/"}),
            (r"/test/(.*)", game_handlers.TestHandler),
        )

        web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    application = Application()
    application.listen(8888)
    ioloop.IOLoop.instance().start()
