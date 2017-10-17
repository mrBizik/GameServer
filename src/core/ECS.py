import copy

from src.core.GameBuilder import Builder
# TODO: EntityList SystemList нафиг не нужны
from src.core.BaseStruct import EntityList, SystemList, TokenList

from src.lib.Observable import Observable


class ECS(Observable):
    def __init__(self, config):
        self.systems = SystemList()
        self.entities = EntityList()
        self.id = None
        self.config = config
        self.is_run = False
        super(ECS, self).__init__()

    def init_game(self):
        system_order = 0
        for system in Builder.build_systems():
            self.systems.push(system, system_order)
            system_order += 1
        for entity in Builder.build_entities(self.config["entities"]):
            self.entities.push(entity)

    def get_config(self, type):
        return self.config

    def set_id(self, identity):
        self.id = identity
        self.config["game_id"] = identity

    def game_loop(self):
        self.is_run = True
        token_list = TokenList()
        self.systems.update_systems(self, 1)
        if not token_list.is_empty():
            self.notify('update', token_list)


class Entity:
    def __init__(self, identity, components_config):
        # TODO: id задается после добавления в ECS объект, необходимо выпилить задание id при создании
        self.id = identity
        self.components = {}
        for config_item in components_config:
            self.components[config_item['name']] = config_item['component']

    def set_id(self, identity):
        self.id = identity

    def add_component(self, name, component, token=None):
        self.components[name] = component
        if token:
            token.set(self.id, name, component.get())

    def update_component(self, name, config, token=None):
        component = self.components[name]
        component.update(config)
        if token:
            token.set(self.id, name, component)

    def update(self, components_config, token=None):
        for name in components_config:
            self.update_component(name, components_config[name], token)

    def get_component(self, name):
        return self.components[name]


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
        return copy.deepcopy(self.values)

    def keys(self):
        return self.values.keys()


class System:
    def __init__(self, config):
        pass

    def update(self, ecs, timestamp):
        raise Exception('Не переопределен метод update для системы!')
