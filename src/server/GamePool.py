import tornado.ioloop as ioloop

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
#

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
            # запускаем румы
            # TODO: лучше запускать руму при входе игроков(?)
            # Вообще лучше отдавать в коллбэк метод из gamePool
            ioloop.IOLoop.instance().add_callback(game.game_loop)
            i += 1

    def _push(self, game):
        self.pool.append(game)
        return len(self.pool)

    def connect_to_game(self, id_game=None):
        game_state = None
        if id_game:
            game_state = self.get_game(id_game)
        else:
            game_state = self.search_game()
        return game_state

    def search_game(self):
        for game in self.pool:
            return game
        return None

    def get_game(self, id_game):
        game_state = None
        try:
            game_state = self.pool[id_game]
        finally:
            return game_state
