import RPCWSocket as Socket
import User

from core.commands.ObjectMove import ObjectMove

class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        self.user = User.UserConnection(application.next_user_id)
        self.game_state = None
        super(GameSocket, self).__init__(application, request, **kwargs)


    def _get_user_conf(self):
      """ Выдать настройки игрока """
        user = self.user
        result = {
           "id": user.id,
           "key_bind": user.key_bind
        }
        return result


    def _on_state_update(self, state):
        # стейт передаем в коллбэк
        # если стейт вычитывать в коллбэке,
        # то есть вероятность вычитать более новую версию,
        # а это не есть хорошо
        self.write_message(state)


    def _close_socket(self):
        self.game_state.leave(self.user.id)


    def  new_game(self, *args):
        self.game_state = self.application.game_pool.new_game()
        self.game_state.add_player(self.user.id, self._on_state_update)
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})


    def connect_game(self, *args):
        params = self._parse_params(["id_game"], *args)
        self.game_state = self.application.game_pool.connect_to_game()
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})


    def move(self, *args):
        params = self._parse_params(["x", "y"], *args)
        params["user"] = self.user.id
        self.game_state.command_push(ObjectMove(params))


    def leave_game(self, *args):
        self.game_state.leave_game(self.user.id)
        self.write_message("leave_game")