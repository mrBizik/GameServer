import queue

from core.GameBuilder import Builder


class ECS:
    def __init__(self, config):
        self.systems = []
        self.entities = []
        self.commands = queue.Queue()
        self.on_update_list = []
        self.id = None
        self.config = config

    def init_game(self):
        system_order = 0
        for system in Builder.build_systems():
            self.add_system(system, system_order)
            system_order += 1
        for entity in Builder.build_entities(self.config["entities"]):
            self.add_entity(entity)

    def get_config(self, type):
        return self.config

    def set_id(self, identity):
        self.id = identity
        self.config["game_id"] = identity

    ''' Add new system into engine '''
    def add_system(self, system, order):
        # my crazy means of system
        system.order = order
        self.systems.append(system)
        self.systems.sort(key=lambda item: item.order)

    ''' Calls every game_loop iteration '''
    def update_systems(self, timestamp):
        for system in self.systems:
            system.update(self, timestamp)

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
        for callback in self.on_update_list:
            callback()

    def add_game_listener(self, callback):
        self.on_update_list.append(callback)


class Entity:
    def __init__(self, identity, components):
        self.id = identity
        self.components = {}
        for component in components:
            self.components[str(type(component))] = component

    def add_component(self, component):
        self.components[str(type(component))] = component

    def update_component(self, name, config, token=None):
        component = self.components[name]
        component.update(config)
        if token:
            token.set(self.id, name, component)

    def update(self, components_config, token=None):
        for name in components_config:
            self.update_component(name, components_config[name], token)

    def __del__(self):
        pass


class Component:
    def __init__(self, keys, config):
        self.values = {}
        self.keys = keys
        self.update(config)

    def update(self, config):
        for key in config.keys():
            # TODO: try catch
            try:
                self.keys.index(key)
                self.values[key] = config[key]
            except ValueError:
              raise Exception('Неверный ключ ' + key + ' class ' + str(self.__class__))

    def get_value(self, key):
        return self.values[key]

    def get(self):
        return self.values

    def keys(self):
        return self.values.keys()

    def __del__(self):
        pass


class System:
    def __init__(self, config):
        pass

    def update(self, ecs, timestamp):
        pass

    def __del__(self):
        pass


class Command:
    def __init__(self, params, player):
        # При создании команды задаем параметры, с которыми она будет выполнятся
        # params можеть быть произвольным объектом, рекомендуется передавать параметры в словаре
        self.params = params
        self.player = player
        # Command.command_list.append(type(self))

    def __call__(self, ecs):
        # Метод переопределяется в предках и выполняет соотв. команде действия
        pass
