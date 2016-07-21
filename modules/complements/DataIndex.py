import modules.complements.GeometryObject as Gobj


class Quadtree:
    def __init__(self, border_rect):
        if type(border_rect) != Gobj.Rectangle:
            raise Exception("Error", "Invalid type border_rect (must Rectangle)")
        self.max_elements_in_node = 5
        self.rect = border_rect
        self.value = []
        self.children = {
            "lt": None,
            "rt": None,
            "rb": None,
            "lb": None
        }

    # Вписывается ли объект в узел
    def _check_object(self, object_rect):
        return self.rect.check_in_rect(object_rect)

    # Разбить узел на дочерние прямоугольники
    def _get_child_rect(self):
        self_size = self.rect.get_size()
        self_position = self.rect.get_position()
        middle_x = self_size[0]/2
        middle_y = self_size[1]/2
        result = {
            "lt": Gobj.Rectangle(middle_x, middle_y, Gobj.Point(self_position[0], self_position[1])),
            "rt": Gobj.Rectangle(middle_x, middle_y, Gobj.Point(self_position[0]+middle_x, self_position[1])),
            "rb": Gobj.Rectangle(middle_x, middle_y, Gobj.Point(self_position[0]+middle_x, self_position[1]+middle_y)),
            "lb": Gobj.Rectangle(middle_x, middle_y, Gobj.Point(self_position[0], self_position[1]+middle_y))
        }

        return result

    def add(self, object_value, object_rect):
        result = False
        child_rect = self._get_child_rect()
        if self._check_object(object_rect):
            if len(self.value) < self.max_elements_in_node:
                self.value.append(object_value)
                result = True
            else:
                if not self.children["lt"]:
                    self.children["lt"] = Quadtree(child_rect["lt"])

                if not self.children["rt"]:
                    self.children['rt'] = Quadtree(child_rect["rt"])

                if not self.children["lb"]:
                    self.children['lb'] = Quadtree(child_rect["lb"])

                if not self.children["rb"]:
                    self.children['rb'] = Quadtree(child_rect["rb"])

                result = self.children["lb"].add(object_value, object_rect)
                result |= self.children["rt"].add(object_value, object_rect)
                result |= self.children["lt"].add(object_value, object_rect)
                result |= self.children["rb"].add(object_value, object_rect)

        return result

    def delete(self, object_value, object_rect):
        result = False
        if self._check_object(object_rect):
            if object_value in self.value:
                self.value.remove(object_value)
                result = True
            else:
                if self.children["lt"]:
                    result = self.children["lt"].delete(object_value, object_rect)

                if self.children["rt"]:
                    result |= self.children["rt"].delete(object_value, object_rect)

                if self.children["lb"]:
                    result |= self.children["lb"].delete(object_value, object_rect)

                if self.children["rb"]:
                    result |= self.children["rb"].delete(object_value, object_rect)

        return result

    def find(self, zone_rect, result):
        if self._check_object(zone_rect):
            if self.value != []:
                result += self.value

            if self.children["lt"]:
                result = self.children["lt"].find(zone_rect, result)
            if self.children["rt"]:
                result = self.children["rt"].find(zone_rect, result)
            if self.children["lb"]:
                result = self.children["lb"].find(zone_rect, result)
            if self.children["rb"]:
                result = self.children["rb"].find(zone_rect, result)

        return result
