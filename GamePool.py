import core.ECS as ECS
import core.GameBuilder as GameBuilder


class GamePool:
    def __init__(self):
        self.pool = []

    def new_game(self):
        game = ECS.ECS()
        game.set_id(self.pool.append(self._init_game(game, None)))
        return game

    def connect_to_game(self, id_game=None):
        game_state = None
        try:
            if id_game:
                game_state = self.pool[id_game]
            else:
                game_state = self.search_game()
        finally:
            return game_state

    def search_game(self):
        for game in self.pool:
            return game
        return None

    def _init_game(self, game, config):
        # TODO: for ECS test
        # for system in GameBuilder.build_system():
        #     game.add_system(system)
        # for entity in GameBuilder.build_entities(config):
        #     game.add_entity(entity)
        return {'id': 1, 'name': 'test'}
