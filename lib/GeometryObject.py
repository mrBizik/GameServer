class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return [self.x, self.y]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self.get_position()

    def get_border_rect(self):
        return None


class Rectangle(Point):
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        position_arr = position.get_position()
        super(Rectangle, self).__init__(position_arr[0], position_arr[1])

    def get_size(self):
        return [self.width, self.height]

    def check_in_point(self, point):
        point_check = (self.x <= point.x) & (self.y <= point.y)
        size_check = (self.x + self.width >= point.x) & (self.y + self.height >= point.y)
        return point_check & size_check

    def check_in_rect(self, rect):
        if type(rect) != Rectangle:
            raise Exception('Error', 'Invalid type rect')

        result = False
        checked_apex = 0
        for i_apex in rect.get_apex():
            if self.check_in_point(i_apex):
                checked_apex += 1

        if checked_apex == 4:
            result = True

        return result

    def get_apex(self):
        """ Возвращает вершины прямоугольника """
        return [
            Point(self.x, self.y),
            Point(self.x + self.width, self.y),
            Point(self.x, self.y + self.height),
            Point(self.x + self.width, self.y + self.height)
        ]

    def check_intersection(self, rect):
        """  Пересекается ли с rect """
        if type(rect) != Rectangle:
            raise Exception('Error', 'Invalid type rect')

        for i_apex in rect.get_apex():
            if self.check_in_point(i_apex):
                return True

        return False

    def get_border_rect(self):
        return self