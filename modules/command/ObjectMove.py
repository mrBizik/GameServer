import modules.command.Command as Command

class ObjectMove(Command.Command):
    def __init__(self, params):
        if params['alias'] != None & params['move_vector'] != None:
            Command.Command.__init__(params)

    def __call__(self, context):
        object_alias = self.params['alias']
        move_vector = self.params['move_vector']
        context.game_objects[object_alias].move(move_vector)
