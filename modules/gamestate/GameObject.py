class GameObject:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    # объект провзаимодействовал с другим объектом
    def action_contact(self):
        return


class DynamicObj(GameObject):
    def __init__(self, width, height, x, y, speed):
        self.speed = speed
        GameObject.__init__(self, width, height, x, y)

    def move(self, move_vector):
        move_vector = move_vector.upper()
        if move_vector == "UP":
            self.x -= self.speed
        if move_vector == "DOWN":
            self.x += self.speed
        if move_vector == "LEFT":
            self.y -= self.speed
        if move_vector == "RIGTH":
            self.y += self.speed
