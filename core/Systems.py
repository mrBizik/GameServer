from core.ECS import System as _System


class CommandSystem(_System):
    def __init__(self, config):
        super(CommandSystem, self).__init__(config)

    def update(self, ecs, timestamp):
        super(CommandSystem, self).update(ecs, timestamp)
        if not ecs.commands.empty():
            command = ecs.commands.get_nowait()
            command(ecs)


class CollisionSystem(_System):
    def __init__(self, config):
        super(CollisionSystem, self).__init__(config)
        self.collision_index = None

    def update(self, ecs, timestamp):
        super(CollisionSystem, self).update(ecs, timestamp)
