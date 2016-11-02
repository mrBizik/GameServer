import lib.GeometryObject as Geometry
import lib.DataIndex as DataIndex

import core.GameObject as Object
from core.Player import Player

import tornado.gen
import tornado.ioloop

import queue


class GameState:
    def __init__(self, width, height):
        self.map_size = Geometry.Rectangle(width, height, Geometry.Point(0, 0))
        self.map_objects = []
        self.map_index = DataIndex.Quadtree(self.map_size)
        # Список игроков, участвующих в игре, необходим для проверки подлиности запросов
        self.players = []
        self.max_players = 4
        self.command_queue = queue.Queue()

    """ Добавить команду в очередь """
    def command_push(self, command):
        self.command_queue.put(command)

    """ Выполнить комманду с контекстом текущего стейта """
    def command_exec(self, command, callback):
         if command:
            print('command_exec ' + str(command.params))
            command(self)

         return callback()

    """ Игровой цикл """
    @tornado.gen.engine
    def game_loop(self):
        command_queue = self.command_queue
        ioloop_instance = tornado.ioloop.IOLoop.instance()
        if not command_queue.empty():
            command = command_queue.get_nowait()
            yield [tornado.gen.Task(self.command_exec, command)]

        self._on_update()
        ioloop_instance.add_callback(self.game_loop)

    def create_map(self, map_objects):
        # TODO: Возможно стоит вообще отказаться от этого метода
        self.map_objects = map_objects

    def add_player(self, user_id, callback = None):
        if not self._is_full():
            # player = Player(user_id, callback, ....)
            self.players.append(player)
            return player
        else:
            raise Exception('Список игроков заполнен!')

    def _is_full(self):
        return not (len(self.players) <= self.max_players)

    def leave(self, id_user):
        pass

    def _on_update(self):
        for player in self.players:
            player.listener()

    def stop_game(self):
        pass
