from core.GameBuilder import Builder
from core.BaseStruct import EntityList, SystemList, TokenList
import copy


class ECS:
    def __init__(self, config):
        self.systems = SystemList()
        self.entities = EntityList()
        self.on_update_list = []
        self.id = None
        self.config = config

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
        token_list = TokenList()
        self.systems.update_systems(self, 1)
        self.fire_update(token_list)

    # TODO: Костыль для обновления слушателей, после выполнения команды
    def fire_update(self, token_list):
        if not token_list.is_empty():
            for callback in self.on_update_list:
                callback(token_list)

    def add_game_listener(self, callback):
        self.on_update_list.append(callback)


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
