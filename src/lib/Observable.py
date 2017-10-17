class Observer:
    def update(self, message, *args):
        pass


class Observable:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def notify(self, message, *args):
        for observer in self.observers:
            observer.update(message, *args)
