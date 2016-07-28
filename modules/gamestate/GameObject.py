import modules.complements.GeometryObject as Gobj


class GameObject:
    def __init__(self, alias, width, height, x, y, speed):
        self.alias = alias
        # Ограничивающий прямоугольник объекта
        # Но т.к. в данной версии движка все объекты прямоугольники
        # то по-сути это размер+позиция объекта
        self.border_rect = Gobj.Rectangle(width, height, Gobj.Point(x, y))
        self.speed = speed

    def move(self, move_vector):
        new_position = self.get_moved_position(move_vector)
        self.border_rect.update_position(new_position)
        return new_position

    def get_moved_position(self, move_vector):
        speed = self.speed
        position = self.border_rect.get_position()
        new_position = Gobj.Point(position[0], position[1])
        if move_vector == 'UP':
            new_position.move(0, (-1) * speed)
        if move_vector == 'DOWN':
            new_position.move(0, speed)
        if move_vector == 'LEFT':
            new_position.move((-1) * speed, 0)
        if move_vector == 'RIGHT':
            new_position.move(speed, 0)

        return new_position

    def collision(self, object_from):
        return True
