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


class Rectangle(Point):
    def __init__(self, width, height, position):
        self.width = width
        self.height = height
        position_arr = position.get_position()
        self.x = position_arr[0]
        self.y = position_arr[1]

    def get_size(self):
        return [self.width, self.height]

    def check_in_point(self, point):
        point_arr = point.get_position()
        point_check = (self.x <= point_arr[0]) & (self.y <= point_arr[1])
        size_check = (self.width >= point_arr[0]) & (self.height >= point_arr[1])
        return point_check & size_check

    def check_in_rect(self, rect):
        if type(rect) != Rectangle:
            raise Exception('Error', 'Invalid type rect')

        result = False
        rect_size_arr = rect.get_size()
        rect_point_arr = rect.get_position()
        if (rect_size_arr[0] <= self.width) & (rect_size_arr[1] <= self.height):
            selfMaxX = self.x + self.width
            rectMaxX = rect_size_arr[0] + rect_point_arr[0]
            if (rect_point_arr[0] >= self.x) & (rectMaxX <= selfMaxX):
                selfMaxY = self.y + self.width
                rectMaxY = rect_size_arr[1] + rect_point_arr[1]
                if (rect_point_arr[1] >= self.y) & (rectMaxY <= selfMaxY):
                    result = True
        return result
