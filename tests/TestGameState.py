import unittest

import lib.GeometryObject as Gobj

import core.GameObject as Object
import core.GameState as Gstate


class GameStateStartTestCase(unittest.TestCase):
    def setUp(self):
        self.state = Gstate.GameState(100, 100)


class DataIndexQuadTreeTestCase(GameStateStartTestCase):
    def test_init_map(self):
        obj_list = [
            Object.GameObject('test1', 50, 50, 0, 0, 1),
            Object.GameObject('test2', 10, 50, 60, 0, 1),
            Object.GameObject('test3', 10, 10, 60, 60, 1)
        ]
        self.state.init_map(obj_list)
        self.assertEqual(len(self.state.game_objects), 3)
        self.assertIsNotNone(self.state.game_objects["test1"])
        self.assertIsNotNone(self.state.game_objects["test2"])
        self.assertIsNotNone(self.state.game_objects["test3"])

    def test_check_collision(self):
        obj_list = [
            Object.GameObject('test1', 50, 50, 0, 0, 1),
            Object.GameObject('test2', 10, 50, 60, 0, 1),
            Object.GameObject('test3', 10, 10, 60, 60, 1)
        ]
        self.state.init_map(obj_list)
        result = self.state.check_collision(Gobj.Rectangle(70, 50, Gobj.Point(0, 0)))
        collision = [
            'test1',
            'test2'
        ]
        self._check_test_collision(result, collision)

        result = self.state.check_collision(Gobj.Rectangle(10, 50, Gobj.Point(0, 0)))
        collision = [
            'test1'
        ]
        self._check_test_collision(result, collision)

        result = self.state.check_collision(Gobj.Rectangle(10, 50, Gobj.Point(20, 0)))
        collision = [
            'test1'
        ]
        self._check_test_collision(result, collision)

        result = self.state.check_collision(Gobj.Rectangle(70, 70, Gobj.Point(0, 0)))
        collision = [
            'test1',
            'test2',
            'test3'
        ]
        self._check_test_collision(result, collision)

    def _check_test_collision(self, result, collision):
        self.assertEqual(len(result), len(collision))
        for i_res in result:
            self.assertIsNotNone(collision.index(i_res.alias))
