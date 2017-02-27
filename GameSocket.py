import RPCWSocket as Socket
import User


class GameSocket(Socket.RPCWSocket):
    def __init__(self, application, request, **kwargs):
        self.user = User.UserConnection(application.next_user_id)
        self.game_state = None
        super(GameSocket, self).__init__(application, request, **kwargs)

    """ Выдать настройки игрока """
    def _get_user_conf(self):
        user = self.user
        result = {
           "id": user.id,
           "key_bind": user.key_bind
        }
        return result

    def _on_state_update(self):
        self.write_message(self.game_state.get_state())

    def _close_socket(self):
        self.game_state.leave(self.user.id)

    def new_game(self, *args):
        self.game_state = self.application.game_pool.new_game()
        self.game_state.add_player(self.user.id, self._on_state_update)
        self.write_message({"ready": True, "state": self.game_state.get_state()})

    def connect_game(self, *args):
        # params = self._parse_params(["id_game"], *args)
        self.game_state = self.application.game_pool.connect_to_game()
        self.write_message({"ready": True, "state": self.game_state.get_state()})

    def move(self, *args):
        # params = self._parse_params(["x", "y"], *args)
        # params["user"] = self.user.id
        # self.game_state.command_push(ObjectMove(params))
        pass

    def leave_game(self, *args):
        self.game_state.leave_game(self.user.id)
        self.write_message("leave_game")