from core.ECS import System as _System


class CollisionSystem(_System):
    def __init__(self, config):
        super(CollisionSystem, self).__init__(config)
        self.collision_index = None

    def update(self, ecs, timestamp):
        pass
