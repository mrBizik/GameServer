import tornado.ioloop
import RPCWSocket as Socket
import User


class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        self.user = User.UserConnection(self.get_secure_cookie("user_id"))
        self.game = None

    def _game_loop(self):
        # TODO: It's all? really? :)
        tornado.ioloop.IOLoop.instance().add_callback(self._game_loop)

    def _on_state_update(self):
        self.write_message(self.game)

    def _close_socket(self):
        pass

    def new_game(self, *args):
        self.game = self.application.game_pool.new_game()
        self._game_loop()
        # TODO: for test ECS
        self.write_message(self.game.id)

    def connect_game(self, *args):
        self.game = self.application.game_pool.connect_to_game()
        self.write_message(self.game)

    def move(self, *args):
        pass

    def leave_game(self, *args):
        pass
