class Observer:
    def __init__(self):
        self.is_ready = True

    def close_observer(self):
        self.is_ready = False

    def update(self, message, *args):
        pass


class Observable:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        self.observers.append(observer)

    def notify(self, message, *args):
        new_observers = []
        for observer in self.observers:
            if observer.is_ready:
                new_observers.append(observer)
                observer.update(message, *args)
        if len(new_observers) > 0:
            self.observers = new_observers
