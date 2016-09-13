import RPCWSocket as Socket
import User

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

    def  new_game(self, *args):
        self.game_state = self.application.game_pool.new_game()
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})

    def connect_game(self, *args):
        params = self._parse_params(["id_game"], *args)
        self.game_state = self.application.game_pool.connect_to_game()
        # TODO: отдать сгенерированный стейт
        self.write_message({"ready": True, "state": None})

    def move(self, *args):
        params = self._parse_params(["x", "y"], *args)
        self.write_message(params)

    def leave_game(self, *args):
        self.game_state.leave_game(self.user.id)
        self.write_message("leave_game")