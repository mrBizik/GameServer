import logging
import tornado.ioloop as ioloop
from src.server.Application import Application
from src.core.GameBuilder import Builder

import src.core.Systems
import src.core.Entities
import src.core.Components


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    Builder.init(src.core.Systems, src.core.Entities, src.core.Components)
    application = Application()
    application.listen(8080)
    ioloop.IOLoop.instance().start()
