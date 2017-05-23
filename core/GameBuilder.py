class Builder:
    entities = None
    components = None
    systems = None

    @staticmethod
    def init(systems_module, entities_module, components_module):
        Builder.entities = Builder._create_module_map(entities_module)
        Builder.components = Builder._create_module_map(components_module)
        Builder.systems = Builder._create_module_map(systems_module)

    @staticmethod
    def _create_module_map(module):
        result = {}
        for class_name in dir(module):
            if Builder._is_build(class_name):
                result[class_name] = eval(".".join(["module", class_name]))
        return result

    @staticmethod
    def _is_build(item_name):
        return not item_name.startswith("_") and item_name != "engine"

    @staticmethod
    def build_entities(conf):
        for item in conf:
            entity_class = Builder.entities[item["type"]]
            entity_components = []
            for component in item["config"]:
                entity_components.append({
                    'component': Builder.create_component(component["type"], component["config"]),
                    'name': component["type"]
                })
            yield entity_class(item["id"], entity_components)

    @staticmethod
    def create_component(type_name, params):
        return Builder.components[type_name](params)

    @staticmethod
    def build_systems():
        for name in Builder.systems:
            yield Builder.systems[name](None)
