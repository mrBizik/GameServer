import lib.GeometryObject as Gobj
import lib.DataIndex as Dindex

import core.GameObject as Object


class GameState:
    def __init__(self, width, height):
        self.size = Gobj.Rectangle(width, height, Gobj.Point(0, 0))
        self.game_objects = {}
        self.map_index = Dindex.Quadtree(self.size)

    # Выполнить комманду с контекстом текущего стейта
    def command_exec(self, command):
         command(self)

    def init_map(self, game_objects):
        #  Заоплняем список игровых объектов и строим индекс расположения объектов
        for i_obj in game_objects:
            if type(i_obj) != Object.GameObject:
                raise Exception('Ошибка инициализации игрового сотояния. Неверный тип игровго оъекта')

            try:
                self.game_objects[i_obj.alias]
            except KeyError:
                self.game_objects[i_obj.alias] = i_obj
                self.map_index.add(i_obj.alias, i_obj.border_rect)
            else:
                raise Exception('Такой alias уже существует')

    # Проверить с кем столкнулся объект for_rect
    def check_collision(self, for_rect):
        result = []
        # Ищем ближайшие объекты
        near_objects = self.map_index.find(for_rect, [])
        # Проверяем с кем пересеклись
        for i_object in near_objects:
            if self.game_objects[i_object].border_rect.check_intersection(for_rect):
                result.append(self.game_objects[i_object])

        return result
