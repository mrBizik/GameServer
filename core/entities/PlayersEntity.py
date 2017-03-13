import core.ECS as ECS


class Player(ECS.Entity):
    def __init__(self, id, config):
        super(Player, self).__init__(id, config)
