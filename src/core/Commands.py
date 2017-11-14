from src.core.BaseStruct import Command


class Move(Command):
    def __call__(self):
        move = self.get_entity().get_component('Move')
        geometry = self.get_entity().get_component('Geometry')
        x2 = self.params['x2']
        y2 = self.params['y2']
        x = geometry.get_value('x')
        y = geometry.get_value('y')
        width = geometry.get_value('width')
        height = geometry.get_value('height')
        if x > x2:
            x -= move.get_value('speed')
        if x < x2:
            x += move.get_value('speed')
        if y > y2:
            y -= move.get_value('speed')
        if y < y2:
            y += move.get_value('speed')

        # TODO: Не очень так проверять столкновения, надо чет получше запилить
        if not self.collision({'x': x, 'y': y, 'width': width, 'height': height}):
            self.get_entity().update({'Geometry': {'x': x, 'y': y}}, self.tokens.new_token())
        super(Move, self).__call__()

    def get_entity(self):
        return self.context.entities.get(self.params['id'])

    def collision(self, a):
        for entity in self.context.entities.get():
            if entity.get_id() != self.get_entity().get_id():
                b = entity.get_component('Geometry').get()
                # TODO: копипаста, проверь!
                x_overlaps = (a['x'] < (b['x'] + b['width'])) and (a['x'] + a['width'] > b['x'])
                y_overlaps = (a['y'] < b['y'] + b['height']) and (a['y'] + a['height'] > b['y'])
                if x_overlaps and y_overlaps:
                    return entity
        return None
