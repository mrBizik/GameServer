from core.GameState import GameState

import tornado.ioloop


class GamePool():
    def __init__(self):
        self.state_pool = []

    def new_game(self):
        ioloop_instance = tornado.ioloop.IOLoop.instance()
        game = GameState(1000, 1000)
        self.state_pool.append(game)
        # закидываем игру в основной цикл сервера
        ioloop_instance.add_callback(game.game_loop)
        return game

    def connect_to_game(self, id_game = None):
        game_state = None
        try:
            if id_game:
                game_state = self.state_pool[id_game]
            else:
                game_state = self._search_game()
        finally:
            return game_state

    def _search_game(self):
        for game in self.state_pool:
            if not game.is_full():
                return game
        return None