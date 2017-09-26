from src.core.ECS import Entity as _Entity


class Player(_Entity):
    def __init__(self, identity, components):
        super(Player, self).__init__(identity, components)
