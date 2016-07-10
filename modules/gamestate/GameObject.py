import modules.complements.GeometryObject as Gobj

class GameObject:
    def __init__(self, width, height, x, y, speed):
        # Ограничивающий прямоугольник объекта
        # Но т.к. в данной версии движка все объекты прямоугольники
        # то по-сути это размер+позиция объекта
        self.border_rect = Gobj.Rectangle(width, height, Gobj.Point(x, y))
        self.speed = speed

    # объект провзаимодействовал с другим объектом
    def action_contact(self):
        return

    def move(self, move_vector):
        return
