class GameState:
    # размер тайла
    tileSize = 30

    def __init__(self, width, height):
        self.currentState = {
            "staticObjects": [],
            "objects": [],
            "mapWidth": width,
            'mapHeight': height
        }

    def add_object(self, game_object):
        object_list = self.currentState["objects"]
        object_list.append(game_object)

    def add_static_object(self, game_object):
        object_list = self.currentState["staticObjects"]
        object_list.append(game_object)
