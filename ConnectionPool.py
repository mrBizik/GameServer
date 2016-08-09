import User

import core.GameState as Game

from lib.SequenceGenerator import Sequence


class GameConnectionPool():
    def __init__(self):
        self.game_pool = []
        self.last_game_id = None
        self.max_players_in_game = 4

    def connect_user_to_game(self, id_user, id_game):
        game = self.get_game(id_game)
        result = None
        if len(game["players"]) <= self.max_players_in_game:
            game["players"].append(id_user)
            self.game_pool[game["id"]] = game
            result = game["id"]
        else:
            raise Exception("Game is full")
        return result

    def new_game(self):
        config = self.get_game_config()
        game = GameState(config["width"], config["height"])
        game.init_map(config["objects"])
        game_pool_object = {
            "id": Sequence().next(),
            "state":game,
            "players":[]
        }
        self.game_pool.append(game_pool_object)
        self.last_game_id = game_pool_object["id"]
        return game_pool_object["id"]

    def get_game_config(self):
        return {
            "width": 100,
            "height": 100,
            "objects": []
        }

    def get_game(self, id_game):
        return self.game_pool[id_game]