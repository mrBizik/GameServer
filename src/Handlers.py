import uuid
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
        self.register_user()
        return self.application.game_pool.get_game_config()

    def register_user(self):
        user_id = self.get_cookie('user_id')
        if not user_id:
            user_id = str(uuid.uuid1())
            self.set_cookie('user_id', user_id)
        logging.debug('register user {}'.format(user_id))
        return user_id


# TODO: Возможно стоит отказаться от наблюдателя, и перенести все в GamePool
class GameSocket(RpcWebSocket, Observer):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        logging.debug('init socket {}'.format(self.get_cookie('user_id')))
        self.user_id = self.get_cookie('user_id')
        self.room = self.application.game_pool.connect_to_room(self.user_id)
        self.room.get_state().register(self)

    def update(self, message, token_list):
        args = None
        if token_list:
            args = token_list.get()

        logging.debug('{} {}'.format(message, args))
        if message == 'update' and self.ws_connection is not None:
            self.send_message(token_list.get())
        super(GameSocket, self).update(message, token_list)

    def rpc_move(self, params):
        params['id'] = 0
        command = Commands.Move(params, self.room.get_state())
        command()

    def on_close(self):
        self.room.delete_player(self.user_id)
        self.close_observer()
