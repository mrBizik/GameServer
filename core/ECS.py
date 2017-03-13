import queue


def sort_by_order(item):
    return item.order


class ECS:
    def __init__(self):
        self.systems = []
        self.entities = []
        self.commands = queue.Queue()
        self.id = None

    def set_id(self, id):
        self.id = id

    ''' Add new system into engine '''
    def add_system(self, system, order):
        # my crazy means of system
        system.order = order
        self.systems.append(system)
        self.systems.sort(key=sort_by_order)

    ''' Calls every game_loop iteration '''
    def update_systems(self, timestamp):
        command = None
        if not self.commands.empty():
            command = self.commands.get_nowait()

        for system in self.systems:
            system.update(self, timestamp, command)

    ''' Push new command for excecute in  future '''
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
    def __init__(self):
        pass

    def update(self, timestamp):
        pass

    def __del__(self):
        pass


class System:
    def __init__(self):
        pass

    def update(self, ecs, timestamp, command):
        pass

    def __del__(self):
        pass