class Sequence():
    def __init__(self):
        self.current_value = -1

    def current(self):
        return self.current_value

    def next(self):
        self.current_value += 1
        return self.current()

    def reset(self):
        self.current_value = -1


class GlobalSequence():
    current_value = -1
    def __init__(self):
        return

    @staticmethod
    def current():
        return GlobalSequence.current_value

    @staticmethod
    def next():
        GlobalSequence.current_value += 1
        return GlobalSequence.current()

    @staticmethod
    def reset():
        GlobalSequence.current_value = -1