from core.ECS import Component as _Component


class Move(_Component):
    def __init__(self, config):
        super(Move, self).__init__(['speed'], config)


class Render(_Component):
    def __init__(self, config):
        # super(Render, self).__init__([], config)
        pass

class Geometry(_Component):
    def __init__(self, config):
        super(Geometry, self).__init__(['x', 'y', 'width', 'height'], config)
