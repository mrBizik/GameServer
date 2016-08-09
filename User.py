from lib.SequenceGenerator import Sequence

import ConnectionPool


class UserConnection():
    def __init__(self, web_socket):
        self.id_game = None
        self.id = Sequence().next()
        self.wsocket = web_socket

    def connect_to_game(self, id_game, pool):
        try:
           self.id_game =  pool.connect_user_to_game(self.id, id_game)
        except Exception:
            # TODO: Сделать поиск свободных игр
            print("Error connect to game")
