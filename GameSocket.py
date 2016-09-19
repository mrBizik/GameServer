import RPCWSocket as Socket
import User

from core.commands.Command import Command

class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        self.user = User.UserConnection(application.next_user_id)
        self.game_state = None
        super(GameSocket, self).__init__(application, request, **kwargs)

    """
      Выдать настройки игрока
    """
    def _get_user_conf(self):
        user = self.user
        result = {
           "id": user.id,
           "key_bind": user.key_bind
        }
        return result

    def _on_state_update(self):
        self.write_message(self.game_state.to_json())

    def  new_game(self, *args):
        # TODO: добавить метод для слушателя
        callback = None
        self.game_state = self.application.game_pool.new_game()
        self.game_state.add_player(self.user.id, callback)
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})

    def connect_game(self, *args):
        params = self._parse_params(["id_game"], *args)
        self.game_state = self.application.game_pool.connect_to_game()
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})

    def move(self, *args):
        params = self._parse_params(["x", "y"], *args)
        command = Command(params)
        command(self)
        print(self.user.id)
        # self.write_message(params)

    def leave_game(self, *args):
        self.game_state.leave_game(self.user.id)
        self.write_message("leave_game")