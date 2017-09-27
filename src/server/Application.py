import tornado.web as web

import src.Handlers as GameHandlers
from src.lib.SequenceGenerator import Sequence
from src.server.GamePool import GamePool


class Application(web.Application):
    def __init__(self):
        # TODO: раздавать так id юзерам плохо. надо переделать
        self.next_user_id = Sequence()
        self.game_pool = GamePool()

        settings = {
            "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            "login_url": "/login",
            # TODO: true
            "xsrf_cookies": False,
            # TODO: не забыть вырубить
            "debug": True
        }

        handlers = (
            (r"/", GameHandlers.IndexHandler),
            (r"/start", GameHandlers.GameHandler),
            (r"/socket/", GameHandlers.GameSocket),
            # (r"/game/(.*)", game_handlers.GameHandler),
            # TODO: разобраться с кэшем, передавать параметром путь до статики(или отдельный конфиг)
            (r"/static/(.*)", web.StaticFileHandler, {"path": "/var/www/static/"})
        )

        web.Application.__init__(self, handlers, **settings)
