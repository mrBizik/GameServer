import core.GameObject
import core.Player
import core.Wall
import core.GameState
import lib.GeometryObject as Geometry

import tornado.ioloop


game_factory_classes = {
    'object': {
        'class': core.GameObject.GameObject
    },
    'player': {
        'class': core.Player.Player
    },
    'wall': {
        'class': core.Wall.Wall
    }
}

test_config = {
    'state': {
        'width': 1100,
        'height': 1100,
    },
    'objects': [
        {
            'class': 'wall',
            'geometry': {
                'width': 10,
                'height': 100,
                'position': [10, 10]
            }
        },
        {
            'class': 'wall',
            'geometry': {
                'width': 100,
                'height': 10,
                'position': [20, 10]
            }
        },
        {
            'class': 'wall',
            'geometry': {
                'width': 100,
                'height': 10,
                'position': [100, 10]
            }
        }
    ]
}


class GamePool:
    def __init__(self):
        self.state_pool = []

    def new_game(self):
        ioloop_instance = tornado.ioloop.IOLoop.instance()
        game = self.build_state(test_config)
        self.state_pool.append(game)
        # закидываем игру в основной цикл сервера
        ioloop_instance.add_callback(game.game_loop)
        return game

    def connect_to_game(self, id_game=None):
        game_state = None
        try:
            if id_game:
                game_state = self.state_pool[id_game]
            else:
                game_state = self._search_game()
        finally:
            return game_state

    def _search_game(self):
        for game in self.state_pool:
            if not game.is_full():
                return game
        return None

    def build_state(self, config):
        new_state = core.GameState.GameState(config['state']['width'], config['state']['height'])
        game_objects = []
        for obj_conf in config['objects']:
            game_objects.append(self.build_object(obj_conf, new_state.map_index))
        new_state.create_map(game_objects)
        return new_state

    def build_object(self, config, map_index):
        object_class = self.get_factory_class(config['class'])
        rect_config = config['geometry']
        point = Geometry.Point(rect_config['position'][0], rect_config['position'][1])
        params = {
            'geometry': Geometry.Rectangle(rect_config['width'], rect_config['height'], point),
            'map_index': map_index
        }
        # TODO: Добавить парсинг доп параметров
        return object_class(**params)

    @staticmethod
    def get_factory_class(class_code):
        return game_factory_classes[class_code]['class']
