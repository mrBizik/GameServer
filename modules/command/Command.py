class Command:
    command_list = []
    # При создании команды задаем параметры, с которыми она будет выполнятся
    # params можеть быть произвольным объектом, рекомендуется передавать параметры в словаре
    def __init__(self, params):
        self.params = params
        Command.command_list.append(type(self))

    # Метод переопределяется в предках и выполняет соотв. команде действия
    def __call__(self, state_context):
        return
