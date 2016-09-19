import lib.GeometryObject as Gobj
import lib.DataIndex as Dindex

import core.GameObject as Object

import tornado.gen

class GameState:
    def __init__(self, width, height):
        self.size = Gobj.Rectangle(width, height, Gobj.Point(0, 0))
        self.game_objects = {}
        self.map_index = Dindex.Quadtree(self.size)
        # Список игроков, участвующих в игре, необходим для проверки подлиности запросов
        self.players = []
        self.max_players = 4
        self.listeners = []

    """ Выполнить комманду с контекстом текущего стейта """
    @tornado.gen.coroutine
    def command_exec(self, command):
        # TODO: Сделать запись в очередь комманд, а вызывать в другом месте(каком?)
         yield command(self)
         self._on_update()

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

    def add_player(self, user_id, callback = None):
        if not self.is_full():
            self.players.append(user_id)
            if callback:
                self.listeners.append(callback)
        else:
            raise Exception('Список игроков заполнен!')

    def is_full(self):
        return not (len(self.players) <= self.max_players)

    def leave(self, id_user):
        pass

    def _on_update(self):
        for listener in self.listeners:
            listener()

