class Command:
    def __init__(self, params, player):
        # При создании команды задаем параметры, с которыми она будет выполнятся
        # params можеть быть произвольным объектом, рекомендуется передавать параметры в словаре
        self.params = params
        self.player = player
        # Command.command_list.append(type(self))

    def __call__(self, state_context):
        # Метод переопределяется в предках и выполняет соотв. команде действия
        pass
