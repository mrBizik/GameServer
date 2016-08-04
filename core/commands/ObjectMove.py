import lib.GeometryObject as Gobj

import core.commands.Command as Command


class ObjectMove(Command.Command):
    def __init__(self, params):
        if params['alias'] & params['move_vector']:
            Command.Command.__init__(params)

    def __call__(self, context):
        result = False
        object_alias, move_vector = self.get_params()
        moved_object = context.game_objects[object_alias]
        size = moved_object.border_rect.get_size()

        # Поиск объектов на новой позиции объекта
        phantom = Gobj.Rectangle(size[0], size[1], moved_object.get_moved_position(move_vector))
        collisions = context.check_collision(phantom, [])
        if collisions == []:
            moved_object.move(move_vector)
            result = True
        else:
            self.send_collision(moved_object, collisions)

        return result

    def send_collision(self, moved_object, collision):
        for i_collision in collision:
            i_collision.collision(moved_object)

    def get_params(self):
        return self.params['alias'], self.params['move_vector']
