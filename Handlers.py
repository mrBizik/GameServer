import tornado.ioloop as ioloop
import tornado.web as web

import RPCWSocket as Socket

import json

import core.Commands as Commands


class TestHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.render('templates/index.html', result=self.get_argument('test'))


class GameHandler(web.RequestHandler):
    def post(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        action = self.get_argument('action')
        params = None
        result = None
        self._register_user()
        if self.get_argument('args'):
            params = json.loads(self.get_argument('args'))

        if action == 'new':
            result = json.dumps({'state': self._new_game()})

        if action == 'connect':
            result = json.dumps({'result': self._connect_to_game(params['idGame'])})

        self.render('templates/index.html', result=result)

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
            # TODO: Беда с куками
            # self.set_cookie('game_id', game.id)
            game_config = game.get_config('frontend')
        return game_config

    def _register_user(self):
        return self.application.next_user_id.next()


class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        super(GameSocket, self).__init__(application, request, **kwargs)
        self.user_id = self.get_secure_cookie('user_id')
        self.game = self.application.game_pool.get_game(self.get_secure_cookie('game_id'))
        self.game.add_game_listener(self._on_game_update)

    def _on_game_update(self):
        self.write_message(self.game)

    def _close_socket(self):
        pass

    def move(self, params):
        self.game.push_command(Commands.Move(params, self.user_id))
