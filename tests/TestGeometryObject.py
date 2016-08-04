import unittest

import lib.GeometryObject as Gobj


class GeometryObjectPointStartTestCase(unittest.TestCase):
    def setUp(self):
        self.point = Gobj.Point(0, 0)


class GeometryObjectPointTestCase(GeometryObjectPointStartTestCase):
    def test_move(self):
        result = self.point.move(2, 1)
        self.assertEqual(self.point.x, 2)
        self.assertEqual(self.point.y, 1)
        self.assertEqual(result, [2, 1])

    def test_get_position(self):
        result = self.point.get_position()
        self.assertEqual(result, [0, 0])


class GeometryObjectRectangleStartTestCase(unittest.TestCase):
    def setUp(self):
        self.point = Gobj.Point(0, 0)
        self.rectangle = Gobj.Rectangle(10, 5, self.point)


class GeometryObjectRectangleTestCase(GeometryObjectRectangleStartTestCase):
    def test_get_size(self):
        result = self.rectangle.get_size()
        self.assertEqual(result, [10, 5])

    def test_check_in_point(self):
        point_in = Gobj.Point(5, 2)
        point_out = Gobj.Point(11, 6)
        self.assertTrue(self.rectangle.check_in_point(point_in))
        self.assertFalse(self.rectangle.check_in_point(point_out))

        point_in = Gobj.Point(10, 5)
        self.assertTrue(self.rectangle.check_in_point(point_in))
        point_in = Gobj.Point(0, 0)
        self.assertTrue(self.rectangle.check_in_point(point_in))
        point_in = Gobj.Point(0, 5)
        self.assertTrue(self.rectangle.check_in_point(point_in))
        point_in = Gobj.Point(10, 0)
        self.assertTrue(self.rectangle.check_in_point(point_in))

    def test_check_in_rect(self):
        rect_in = Gobj.Rectangle(1, 1, Gobj.Point(5, 2))
        rect_out = Gobj.Rectangle(1, 1, Gobj.Point(11, 6))
        self.assertTrue(self.rectangle.check_in_rect(rect_in))
        self.assertFalse(self.rectangle.check_in_rect(rect_out))

        rect_out = Gobj.Rectangle(15, 5, Gobj.Point(5, 2))
        self.assertFalse(self.rectangle.check_in_rect(rect_out))
        rect_out = Gobj.Rectangle(5, 15, Gobj.Point(5, 2))
        self.assertFalse(self.rectangle.check_in_rect(rect_out))
        rect_out = Gobj.Rectangle(5, 15, Gobj.Point(0, 0))
        self.assertFalse(self.rectangle.check_in_rect(rect_out))

        rect_in = Gobj.Rectangle(10, 5, Gobj.Point(0, 0))
        self.assertTrue(self.rectangle.check_in_rect(rect_in))
        rect_in = Gobj.Rectangle(5, 5, Gobj.Point(5, 0))
        self.assertTrue(self.rectangle.check_in_rect(rect_in))
        rect_in = Gobj.Rectangle(5, 2, Gobj.Point(5, 1))
        self.assertTrue(self.rectangle.check_in_rect(rect_in))

        self.rectangle = Gobj.Rectangle(50, 50, Gobj.Point(50, 0))
        rect_in = Gobj.Rectangle(25, 25, Gobj.Point(25, 0))
        self.assertFalse(self.rectangle.check_in_rect(rect_in))

        self.rectangle = Gobj.Rectangle(50, 50, Gobj.Point(50, 0))
        rect_in = Gobj.Rectangle(25, 25, Gobj.Point(75, 0))
        self.assertTrue(self.rectangle.check_in_rect(rect_in))
