from core.GameObject import GameObject


class Player(GameObject):
    def __init__(self, user_id, listener_callback, geometry, speed, map_index):
        self.user_id = user_id
        self.listener = listener_callback
        super(Player, self).__init__(geometry, speed, map_index)

    def get(self):
        attr = super(Player, self).get()
        attr['user_id'] = self.user_id
        return attr
