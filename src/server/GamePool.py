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
                        "width": 128,
                        "height": 128,
                        "x": 128,
                        "y": 128,
                    }
                },
                {
                    "type": "Render",
                    "config": {
                        "width": 512,
                        "height": 128,
                        "x": 0,
                        "y": 0,
                        "speed": 20,
                        "frameCount": 4,
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
        "atlas": "./img/smurfic.jpg",
        "sound": []
    }
}


class GamePool:
    def __init__(self):
        self.pool = []
        Builder.init(src.core.Systems, src.core.Entities, src.core.Components)

    def _push(self, game):
        self.pool.append(game)
        return len(self.pool)

    def new_game(self):
        game = ECS(_config)
        game.init_game()
        game.set_id(self._push(game))
        return game

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
