import unittest

import modules.complements.DataIndex as DIndex

import modules.complements.GeometryObject as Gobj


class DataIndexQuadtreeStartTestCase(unittest.TestCase):
    def setUp(self):
        point = Gobj.Point(0, 0)
        map = Gobj.Rectangle(100, 100, point)
        self.tree = DIndex.Quadtree(map)
        self.tree.max_elements_in_node = 1


class DataIndexQuadTreeTestCase(DataIndexQuadtreeStartTestCase):
    def test_add(self):
        test_object = {
            "value": "test_value",
            "rect": Gobj.Rectangle(50, 50, Gobj.Point(50, 0))
        }
        self.assertTrue(self.tree.add(test_object["value"], test_object["rect"]))

        test_object_2 = {
            "value": "test_value_2",
            "rect": Gobj.Rectangle(20, 20, Gobj.Point(0, 0))
        }
        self.assertTrue(self.tree.add(test_object_2["value"], test_object_2["rect"]))

        self.assertIsNotNone(self.tree.children["rt"])
        self.assertIsNotNone(self.tree.children["lt"])
        self.assertIsNotNone(self.tree.children["lb"])
        self.assertIsNotNone(self.tree.children["rb"])
        self.assertEqual(self.tree.value, [test_object["value"]])

        lt_branch = self.tree.children["lt"]
        self.assertIsNone(lt_branch.children["rt"])
        self.assertIsNone(lt_branch.children["lt"])
        self.assertIsNone(lt_branch.children["lb"])
        self.assertIsNone(lt_branch.children["rb"])
        self.assertEqual(lt_branch.value, [test_object_2["value"]])

    def test_find(self):
        test_object = [
            {
                "value": "test_value",
                "rect": Gobj.Rectangle(50, 50, Gobj.Point(50, 0))
            },
            {
                "value": "test_value_2",
                "rect": Gobj.Rectangle(20, 20, Gobj.Point(0, 0))
            },
            {
                "value": "test_value_3",
                "rect": Gobj.Rectangle(20, 20, Gobj.Point(70, 0))
            },
            {
                "value": "test_value_4",
                "rect": Gobj.Rectangle(10, 10, Gobj.Point(70, 70))
            }
        ]

        for obj in test_object:
            self.tree.add(obj["value"], obj["rect"])

        result = self.tree.find(Gobj.Rectangle(50, 50, Gobj.Point(50, 0)), [])
        self.assertEqual(result, [test_object[0]["value"], test_object[2]["value"]])

    def test_delete(self):
        test_object = [
            {
                "value": "test_value",
                "rect": Gobj.Rectangle(50, 50, Gobj.Point(50, 0))
            },
            {
                "value": "test_value_2",
                "rect": Gobj.Rectangle(20, 20, Gobj.Point(0, 0))
            },
            {
                "value": "test_value_3",
                "rect": Gobj.Rectangle(20, 20, Gobj.Point(70, 0))
            },
            {
                "value": "test_value_4",
                "rect": Gobj.Rectangle(10, 10, Gobj.Point(70, 70))
            }
        ]

        for obj in test_object:
            self.tree.add(obj["value"], obj["rect"])

        check = self.tree.find(Gobj.Rectangle(50, 50, Gobj.Point(50, 0)), [])
        self.assertTrue(self.tree.delete(test_object[0]["value"], Gobj.Rectangle(50, 50, Gobj.Point(50, 0))))
        result = self.tree.find(Gobj.Rectangle(50, 50, Gobj.Point(50, 0)), [])
        self.assertEqual(self.diff(check, result), [test_object[0]["value"]])

    def diff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]
