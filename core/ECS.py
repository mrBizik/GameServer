import queue

from core.GameBuilder import Builder


class ECS:
    def __init__(self, config):
        self.systems = []
        self.entities = []
        self.commands = queue.Queue()
        self.id = None
        self.config = config

    def init_game(self):
        for system in Builder.build_systems():
            # TODO: order!!!
            self.add_system(system, 1)
        for entity in Builder.build_entities(self.config["entities"]):
            self.add_entity(entity)

    def get_config(self, type):
        return self.config

    def set_id(self, id):
        self.id = id

    ''' Add new system into engine '''
    def add_system(self, system, order):
        # my crazy means of system
        system.order = order
        self.systems.append(system)
        self.systems.sort(key=lambda item: item.order)

    ''' Calls every game_loop iteration '''
    def update_systems(self, timestamp):
        command = None
        if not self.commands.empty():
            command = self.commands.get_nowait()

        for system in self.systems:
            system.update(self, timestamp, command)

    ''' Push new command for execute in  future '''
    def push_command(self, command):
        self.commands.put_nowait(command)

    ''' Add new entity '''
    def add_entity(self, entity):
        self.entities.append(entity)

    def drop_entity(self, id):
        pass

    def find_entity(self, id):
        for entity in self.entities:
            if entity.id == id:
                return entity

    def game_loop(self):
        self.update_systems(1)


class Entity:
    def __init__(self, id, components):
        self.id = id
        self.components = {}
        for component in components:
            self.components[str(type(component))] = component

    def add_component(self, component):
        self.components[str(type(component))] = component

    def __del__(self):
        pass


class Component:
    def __init__(self, config):
        pass

    def update(self, timestamp):
        pass

    def __del__(self):
        pass


class System:
    def __init__(self, config):
        pass

    def update(self, ecs, timestamp, command):
        pass

    def __del__(self):
        pass
