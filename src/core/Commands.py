from src.core.BaseStruct import Command


class Move(Command):
    def __call__(self):
        entity = self.context.entities.get(self.params['id'])
        move = entity.get_component('Move')
        geometry = entity.get_component('Geometry')
        x1 = self.params['x1']
        y1 = self.params['y1']
        x2 = self.params['x2']
        y2 = self.params['y2']
        x = geometry.get_value('x')
        y = geometry.get_value('y')
        if x1 > x2:
            x -= move.get_value('speed')
        else:
            x += move.get_value('speed')
        if y1 > y2:
            y -= move.get_value('speed')
        else:
            y += move.get_value('speed')

        entity.update({'Geometry': {'x': x, 'y': y}}, self.tokens.new_token())
        self.context.fire_update(self.tokens)
