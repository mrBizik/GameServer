from core.GameObject import GameObject


class Wall(GameObject):
    def __init__(self, geometry, map_index):
        super(Wall, self).__init__(geometry, 0, map_index)
