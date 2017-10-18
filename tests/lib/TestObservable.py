import unittest

from src.lib.Observable import Observer, Observable


class ObserverTestCase(unittest.TestCase):
    def test_create(self):
        observer = Observer()
        self.assertTrue(observer.is_ready)

    def test_update(self):
        observer = Observer()

        def mock_update(message, *args):
            return message == 'test'

        observer.update = mock_update
        self.assertTrue(observer.update('test'))

    def test_close_observer(self):
        observer = Observer()
        observer.close_observer()
        self.assertFalse(observer.is_ready)


class ObservableTestCase(unittest.TestCase):
    def test_register(self):
        observable = Observable()
        observer = Observer()
        observable.register(observer)
        self.assertEqual(len(observable.observers), 1)
        self.assertEqual(observable.observers, [observer])

    def test_notify_one(self):
        observable = Observable()
        observer = Observer()
        update_calls = []
        notify_msg = ['1', '2', '3', '4']

        def mock_update(message, *args):
            update_calls.append(message)

        observer.update = mock_update
        observable.register(observer)

        for msg in notify_msg:
            observable.notify(msg)
        self.assertEqual(update_calls, notify_msg)

    def test_notify_many(self):
        observable = Observable()
        observer1 = Observer()
        observer2 = Observer()
        update_calls = []

        def mock_update_1(message, *args):
            update_calls.append('{} 1'.format(message))

        def mock_update_2(message, *args):
            update_calls.append('{} 2'.format(message))

        observer1.update = mock_update_1
        observable.register(observer1)
        observer2.update = mock_update_2
        observable.register(observer2)

        observable.notify('ok')
        self.assertEqual(update_calls, ['ok 1', 'ok 2'])

    def test_notify_when_closed(self):
        observable = Observable()
        observer1 = Observer()
        observer2 = Observer()
        update_calls = []

        def mock_update_1(message, *args):
            update_calls.append('{} 1'.format(message))

        def mock_update_2(message, *args):
            update_calls.append('{} 2'.format(message))

        observer1.update = mock_update_1
        observable.register(observer1)
        observer2.update = mock_update_2
        observable.register(observer2)
        observer2.is_ready = False
        observable.notify('ok')
        self.assertEqual(update_calls, ['ok 1'])
