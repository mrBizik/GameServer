import RPCWSocket as Socket
import User

class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        self.user = User.UserConnection(application.next_user_id)
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

    def  new_game(self, params):
        self.write_message(1)

    def connect_game(self, params):
        params = self._parse_params(["id_game"], params)
        self.write_message("connect_game")

    def move(self, params):
        params = self._parse_params(["x", "y"], params)
        self.write_message(params)

    def disconnect_game(self):
         self.write_message("disconnect_game")