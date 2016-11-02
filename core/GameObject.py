import lib.GeometryObject as Geometry


class GameObject:
    def __init__(self, geometry, speed, map_index, graphic):
        self.geometry_model = geometry
        self.map_index = map_index
        self.bored = []
        self.speed = speed
        # графика
        self.graphic_model = graphic
        # добавляем статический объект в мап индекс
        if speed == 0:
            map_index.add(self, self.geometry_model.get_border_rect())

    def __del__(self):
        self.map_index.delete(self, self.geometry_model.get_border_rect())

    def get_geometry(self):
        return self.geometry_model

    def move(self, move_vector):
        point = self._get_vector_speed(move_vector)
        size = self.geometry_model.get_size()
        old_position = self.geometry_model.get_border_rect().get_position()
        old_rect = Geometry.Rencagle(size[0], size[1], Geometry.Point(old_position[0], old_position[1]))
        new_rect = old_rect
        # проверяем можно ли переместиться в заданную точку
        self.bored = self._bordered_object(point)
        if len(self.bored) == 0:
            new_position = self.geometry_model.move(point.x, point.y)
            new_rect = Geometry.Rencagle(size[0], size[1], Geometry.Point(new_position[0], new_position[1]))
            self.map_index.update(self, old_rect, new_rect)
        else:
            self.collisions()
        return new_rect

    """ Для преобразования в строку и дальнешей отправки клиенту """
    def parse(self):
        pass

    """ Проверить нет ли объекта в том месте, куда хотим сдвинуться """
    def _bordered_object(self, move_point):
        size = self.geometry_model.get_size()
        position = self.geometry_model.get_border_rect().get_position()
        rect = Geometry.Rencagle(size[0], size[1], Geometry.Point(position[0], position[1]))
        rect.move(move_point[0], move_point[1])
        return self.map_index.find(rect, [])

    def collisions(self):
        for obj in self.bored:
            self._is_collision(obj)

    """ Выполнить действия в зависимости от объекта, с которыми столкнулись """
    def _is_collision(self, obj):
        pass

    def _get_vector_speed(self, move_vector):
        speed = self.speed
        if move_vector == 'UP':
            return Geometry.Point(0, -1 * speed)
        elif move_vector == 'DOWN':
            return Geometry.Point(0, speed)
        elif move_vector == 'LEFT':
            return Geometry.Point(-1 * speed, 0)
        elif move_vector == 'RIGHT':
            return Geometry.Point(speed, 0)
        else:
            return Geometry.Point(0, 0)
