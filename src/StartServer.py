import tornado.ioloop as ioloop
from src.server.Application import Application


if __name__ == "__main__":
    application = Application()
    application.listen(8080)
    ioloop.IOLoop.instance().start()
