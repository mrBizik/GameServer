import modules.complements.GeometryObject as Gobj
import modules.gamestate.GameObject as Object
import modules.complements.DataIndex as Dindex

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

            self.game_objects[i_obj.alias] = i_obj
            self.map_index.add(i_obj.alias, i_obj.border_rect)

    def check_colision(self, for_object):
        return