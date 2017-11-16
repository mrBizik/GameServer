from src.core.ECS import System as _System


# TODO:
# Пока система не нужна
# Думаю использовать ее как постоитель индекса объектов (QuadTree, RTree или еще что...)
# Идея такая:
# При движении просить у системы объекты "в радиусе конечной точки перемещения" и тем самым уменьшат кол-во сравнений
# Дерево перестраивать не на каждое перемещение, а раз в N итераций или по требованию.
# То что оно не совсем точно наверное не страшно
class CollisionSystem(_System):
    def __init__(self, config):
        super(CollisionSystem, self).__init__(config)
        self.collision_index = None

    def update(self, ecs, timestamp):
        pass
