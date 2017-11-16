import logging


class EntityList:
    def __init__(self):
        self.entities = []

    def push(self, entity):
        self.entities.append(entity)
        id = len(self.entities) - 1
        entity.set_id(id)

    def get(self, identity = None):
        if identity is not None:
            return self.entities[identity]
        else:
            return self.entities


class SystemList:
    def __init__(self):
        self.systems = []

    def push(self, system, order):
        system.order = order
        self.systems.append(system)

    def order(self):
        self.systems.sort(key=lambda item: item.order)

    def update_systems(self, context, timestamp):
        for system in self.systems:
            system.update(context, timestamp)


class Token:
    def __init__(self):
        self.id_entity = None
        self.component_values = None
        self.component_name = None
        self.timestamp = None

    def set(self, id_entity, component_name, component, timestamp = 0):
        if self.id_entity:
            raise Exception('Токен уже использовался')
        self.id_entity = id_entity
        self.component_values = component.get()
        self.component_name = component_name
        self.timestamp = timestamp

    def get(self):
        return {
            'id': self.id_entity,
            'component_name': self.component_name,
            'component': self.component_values,
            'timestamp': self.timestamp
        }


class TokenList:
    def __init__(self):
        self.tokens = []

    def new_token(self):
        token = Token()
        self.tokens.append(token)
        return token

    def get(self):
        result = []
        self.tokens.sort(key=lambda item: item.timestamp)
        # TODO: А может через token.get()?
        # return self.tokens
        for token in self.tokens:
            result.append(token.get())
        return result

    def is_empty(self):
        return len(self.tokens) == 0


# TODO: нужны геттеры для параметров
class Command:
    def __init__(self, params, context, tokenize=True):
        # При создании команды задаем параметры, с которыми она будет выполнятся
        # params можеть быть произвольным объектом, рекомендуется передавать параметры в словаре
        if not context:
            raise Exception('Не указан context')
        self.params = params
        self.context = context
        self.tokens = None
        # Если необходимо фиксировать изменеия, то создадим токен лист
        if tokenize:
            self.tokens = TokenList()

    def __call__(self, extra_args=None):
        log = logging.getLogger('core.Command')
        self.context.notify('update', self.tokens)
        log.debug('call command {}({}) extra_args: {}'.format(self.__class__, self.params, extra_args))

    def notify_game(self, message, *args):
        self.context.notify(message, *args)
