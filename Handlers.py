import tornado.ioloop as ioloop
import tornado.web as web

import RPCWSocket as Socket

import json


class TestHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.render("templates/index.html", result=self.get_argument("test"))


class GameHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        action = self.get_argument("action")
        params = None
        result = None
        if self.get_argument("args"):
            params = json.loads(self.get_argument("args"))

        if action == "new":
            result = json.dumps({"state": self._new_game()})

        if action == "connect":
            result = json.dumps({"result": self._connect_to_game(params["idGame"])})

        self.render("templates/index.html", result=result)

    def _connect_to_game(self, id_game):
        return self.application.game_pool.connect_to_game(id_game)

    def _new_game(self):
        game_config = None
        game = self.application.game_pool.new_game()
        if game:
            ioloop.IOLoop.instance().add_callback(game.game_loop)
            self._connect_to_game(game.id)
            game_config = game.get_config('frontend')
        return game_config


class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        # self.user = User.UserConnection(self.get_secure_cookie("user_id"))
        self.game = None
    #
    # def _game_loop(self):
    #     # TODO: It's all? really? :)
    #     tornado.ioloop.ioloop.instance().add_callback(self._game_loop)

    # def _on_state_update(self):
    #     self.write_message(self.game)

    def _close_socket(self):
        pass

    # def new_game(self, *args):
    #     self.game = self.application.game_pool.new_game()
    #     self._game_loop()
    #     # TODO: for test engine
    #     self.write_message(self.game.id)

    # def connect_game(self, *args):
    #     self.game = self.application.game_pool.connect_to_game()
    #     self.write_message(self.game.get_config("frontend"))

    def move(self, *args):
        # self.game.push_command('move')
        pass

    # def leave_game(self, *args):
    #     pass
