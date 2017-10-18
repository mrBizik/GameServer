import logging
import tornado.web as web

from src.core import Commands
from src.server.JSONRpc import RpcWebSocket, RpcHandler
from src.lib.Observable import Observer


class IndexHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('server/templates/index.html', title="ECS engine", canvas={
            "id": "test-canvas",
            "width": 700,
            "height": 700
        })


class GameHandler(RpcHandler):
    def rpc_connect_to_game(self, params):
        game_config = None
        id_game = params['idGame']
        game = self.application.game_pool.connect_to_game(id_game)
        if game:
            game_config = game.get_config('frontend')
        return game_config

    def register_user(self):
        if not self.get_cookie('user_id'):
            self.set_cookie('user_id', '1')


class GameSocket(RpcWebSocket, Observer):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        # self.user_id = self.get_cookie('user_id')
        # TODO: hardcode
        self.user_id = 1
        self.game = self.application.game_pool.get_game(0)
        self.game.register(self)

    def update(self, message, token_list):
        # TODO: временный костыль пока нормальное завершение игры не сделаю
        if message == 'update' and self.ws_connection is not None:
            logging.debug('update {}'.format(token_list.get()))
            self.send_message(token_list.get())

    def rpc_move(self, params):
        # TODO: Не факт что сущность равна id_user
        # params['id'] = self.user_id
        params['id'] = 0
        command = Commands.Move(params, self.game)
        command()

    def on_close(self):
        self.close_observer()
