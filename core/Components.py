from core.ECS import Component as _Component


class Move(_Component):
    def __init__(self, config):
        super(Move, self).__init__(config)
        self.speed = config['speed']


class Render(_Component):
    def __init__(self, config):
        super(Render, self).__init__(config)


class Geometry(_Component):
    def __init__(self, config):
        super(Geometry, self).__init__(config)
        self.x = config['x']
        self.y = config['y']
        self.width = config['width']
        self.height = config['height']
