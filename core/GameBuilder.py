import core.Systems
import core.Components
import core.Entities


class Builder:
    def __init__(self):
        self.entities = self._create_class_map(core.Entities, 'core.Entities')
        self.components = self._create_class_map(core.Components, 'core.Components')
        self.systems = self._create_class_map(core.Systems, 'core.Systems')

    def _create_class_map(self, module, module_name):
        result = {}
        for class_name in dir(module):
            if self._is_builded(class_name):
                class_obj = self._get_module_item([module_name, class_name])
                result[class_name] = class_obj
        return result

    @staticmethod
    def _get_module_item(path):
        return eval('.'.join(path))

    @staticmethod
    def _is_builded(item_name):
        return not item_name.startswith('_') and item_name != 'ECS'

    def build_entities(self, config):
        for item in config:
            entity_class = self.entities[item['type']]
            entity_components = []
            for comp in item['config']:
                entity_components.append(self.create_component(comp))

            yield entity_class(item['id'], entity_components)

    def create_component(self, config):
        return config

    def build_systems(self):
        # for system in system_arr:
        #     yield system()
        pass


if __name__ == '__main__':
    config = [
        {
            'type': 'Player',
            'config': [],
            'id': 1
        },
        {
            'type': 'Player',
            'config': [],
            'id': 2
        }
    ]
    builder = Builder()
    print(str(builder.entities))
    for entity in builder.build_entities(config):
        print(str(entity.id))
