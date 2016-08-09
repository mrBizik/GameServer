class Sequence():
    current_value = None
    def __init__(self):
        return

    def current(self):
        return Sequence.current_value

    def next(self):
        if not Sequence.current_value:
            Sequence.init_sequence()
        Sequence.current_value += 1
        return Sequence.current()

    def reset(self):
        Sequence.current_value = -1

    def init_sequence(self):
        Sequence.current_value = -1