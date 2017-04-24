class Token:
    def __init__(self):
        self.id_entity = None
        self.components = []

    def set(self, id_entity, component_name, component):
        if self.id_entity:
            raise Exception('Токен уже использовался id_entity=' + self.id_entity)
        self.id_entity = id_entity
        self.components.append({component_name: component})

    def get(self):
        return {
            'id': self.id_entity,
            'components': self.components
        }