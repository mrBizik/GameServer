import tornado.ioloop as ioloop
import tornado.web as web

from src.core import Commands
from src.server import RPCWSocket as Socket


class IndexHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('templates/index.html', title="ECS engine", canvas={
            "id": "test-canvas",
            "width": 700,
            "height": 700
        })


class GameHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        action = self.get_argument('action')
        params = None
        result = None
        self._register_user()
        if self.get_argument('args'):
            params = json.loads(self.get_argument('args'))

        if action == 'new':
            result = {'state': self._new_game()}

        if action == 'connect':
            result = {'result': self._connect_to_game(params['idGame'])}

        self.render('templates/answer.html', result=result)

    def _connect_to_game(self, id_game):
        game_config = None
        game = self.application.game_pool.connect_to_game(id_game)
        if game:
            game_config = game.get_config('frontend')
        return game_config

    def _new_game(self):
        game_config = None
        game = self.application.game_pool.new_game()
        if game:
            ioloop.IOLoop.instance().add_callback(game.game_loop)
            self._connect_to_game(game.id)
            # self.set_cookie('game_id', str(game.id))
            game_config = game.get_config('frontend')
        return game_config

    def _register_user(self):
        if not self.get_cookie('user_id'):
            self.set_cookie('user_id', str(self.application.next_user_id.next()))


class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        # self.user_id = self.get_cookie('user_id')
        # TODO: hardcode
        self.user_id = 1
        self.game = self.application.game_pool.get_game(0)
        self.game.add_game_listener(self._on_game_update)

    def _on_game_update(self, token_list):
        # TODO: временный костыль пока нормальное завершение игры не сделаю
        if self.ws_connection is not None:
            self.write_message(token_list.get())

    def _close_socket(self):
        print('close_socket')

    def move(self, params):
        # TODO: Не факт что сущность равна id_user
        # params['id'] = self.user_id
        params['id'] = 0
        command = Commands.Move(params, self.game)
        command()
