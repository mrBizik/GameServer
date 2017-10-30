import tornado.ioloop as ioloop
from tornado import gen

from src.core.ECS import ECS

import uuid
import copy
import logging

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


class GameRoom:
    def __init__(self, game_config):
        self.id = str(uuid.uuid1())
        self.game = ECS()
        self.config = copy.deepcopy(game_config)
        self.config["game_id"] = self.get_id()
        self.game.init_game(game_config)
        self.players = []

    def get_config(self):
        return self.config

    def get_state(self):
        return self.game

    def get_id(self):
        return self.id

    def add_player(self, player):
        if not self.game.is_run:
            self.start_game()
        logging.debug('add_player {}'.format(player))
        if not self.check_player(player):
            self.players.append(player)

    def delete_player(self, player):
        new_list = []
        logging.debug('add_player {}'.format(player))
        # TODO: убрать костыль
        for item in self.players:
            if player != item:
                new_list.append(player)
        self.players = new_list

    def start_game(self):
        self.game.start_game()
        # 1 ядро грузится на 100%
        # ioloop.IOLoop.current().spawn_callback(self._game_loop)

    @gen.coroutine
    def _game_loop(self):
        while self.game.is_run and len(self.players) > 0:
            yield self.game.game_loop()
        self.stop_game()

    def stop_game(self):
        self.game.stop_game()

    def check_player(self, player):
        result = False
        for p in self.players:
            if p == player:
                result = True
        return result


class GamePool:
    def __init__(self):
        self.game_limit = 2
        self.pool = []
        i = 0
        while i < self.game_limit:
            self.pool.append(GameRoom(_config))
            i += 1

    def connect_to_room(self, player, id_game=None):
        if id_game:
            room = self.get_room(id_game, player)
        else:
            room = self.search_room()

        if room is not None:
             room.add_player(player)

        return room

    def search_room(self):
        return self.pool[0]

    def get_room(self, id_game, player):
        for room in self.pool:
            if room.get_id() == id_game and room.check_player(player):
                return room

    def get_game_config(self):
        # TODO: Хранить в базе
        return _config
