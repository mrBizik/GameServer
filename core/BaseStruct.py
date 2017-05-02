class EntityList:
    def __init__(self):
        self.entities = []

    def push(self, entity):
        self.entities.append(entity)
        id = len(self.entities) - 1
        entity.set_id(id)

    def get(self, identity):
        # TODO: try catch + проверка на отрицательные значения(?)
        return self.entities[identity]


class SystemList:
    def __init__(self):
        self.systems = []

    def push(self, system, order):
        system.order = order
        self.systems.append(system)

    def order(self):
        self.systems.sort(key=lambda item: item.order)

    def update_systems(self, timestamp):
        for system in self.systems:
            system.update(self, timestamp)


class Token:
    def __init__(self):
        self.id_entity = None
        self.components = None

    def set(self, id_entity, component_name, component):
        if self.id_entity and self.id_entity != id_entity:
            raise Exception('Токен уже использовался с другой сущьностью id_entity=' + self.id_entity)
        self.id_entity = id_entity
        self.components.append({component_name: component})

    def get(self):
        return {
            'id': self.id_entity,
            'components': self.components
        }


class TokenList:
    def __init__(self):
        self.tokens = []

    def new(self):
        token = Token()
        self.tokens.append(token)
        return token

    def get(self):
        result = []
        for token in self.tokens:
            result.append(token.get())
        return result

    def is_empty(self):
        return len(self.tokens) == 0


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
        # Метод переопределяется в предках и выполняет соотв. команде действия
        raise Exception('Не переопределен метод __call__ для команды!')
