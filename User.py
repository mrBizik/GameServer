class UserConnection():
    def __init__(self, user_seq):
        # TODO: Вытаскивать юзера из базы и выдавать все настройки
        self.key_bind = self.init_key_bind()
        self.id = user_seq.next()


    def init_key_bind(self):
        """ Получить раскладку клавиш для пользователя """
        # TODO: Вытаскивать из базы
        return {}