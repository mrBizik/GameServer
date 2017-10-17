import tornado.ioloop as ioloop
from tornado import gen

from src.core.GameBuilder import Builder

from src.core.ECS import ECS

import src.core.Systems
import src.core.Entities
import src.core.Components


_config = {
    "entities": [
        {
            "type": "Player",
            # TODO: Idшники выставляются во время создания сущностей, надо чтобы на фронт попадало все верно
            "id": 0,
            "config": [
                {
                    "type": "Geometry",
                    "config": {
                        "width": 96,
                        "height": 174,
                        "x": 128,
                        "y": 128,
                    }
                },
                {
                    "type": "Render",
                    "config": {
                        "width": 1024,
                        "height": 220,
                        "x": 0,
                        "y": 0,
                        "speed": 20,
                        "frameCount": 10,
                        "animationSpeed": 10
                    }
                },
                {
                    "type": "Move",
                    "config": {
                        "speed": 10
                    }
                }
            ]
        },
        {
            "type": "Player",
            # TODO: Idшники выставляются во время создания сущностей, надо чтобы на фронт попадало все верно
            "id": 1,
            "config": [
                {
                    "type": "Geometry",
                    "config": {
                        "width": 96,
                        "height": 174,
                        "x": 200,
                        "y": 128,
                    }
                },
                {
                    "type": "Render",
                    "config": {
                        "width": 1024,
                        "height": 220,
                        "x": 0,
                        "y": 220,
                        "speed": 20,
                        "frameCount": 10,
                        "animationSpeed": 10
                    }
                },
                {
                    "type": "Move",
                    "config": {
                        "speed": 10
                    }
                }
            ]
        }
    ],
    "resources": {
        "atlas": "/static/chicken.jpg",
        "sound": []
    }
}


#TODO: План доработки:
# Здесь будет:
# - вытаскивание конфигов игры из базы
# - запуск рум при входе игроков (а правильнее по команде start_game)

class GamePool:
    def __init__(self):
        self.game_limit = 2
        self.pool = []
        Builder.init(src.core.Systems, src.core.Entities, src.core.Components)
        i = 0
        while i < self.game_limit:
            game = ECS(_config)
            game.init_game()
            game.set_id(self._push(game))
            i += 1

    @gen.coroutine
    def game_pool_loop(self):
        i = 0
        while True:
            game = self.pool[i]
            if game.is_run:
                yield game.game_loop()
            i += 1
            if i == len(self.pool):
                i = 0

    def _push(self, game):
        self.pool.append(game)
        return len(self.pool)

    def connect_to_game(self, id_game=None):
        if id_game:
            game_state = self.get_game(id_game)
        else:
            game_state = self.search_game()
        game_state.is_run = True
        ioloop.IOLoop.current().spawn_callback(self.game_pool_loop)
        return game_state

    def search_game(self):
        for game in self.pool:
            return game
        return None

    def get_game(self, id_game):
        return self.pool[0]
        # game_state = None
        # try:
        #     game_state = self.pool[id_game]
        # finally:
        #     return game_state
