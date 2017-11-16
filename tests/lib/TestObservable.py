import unittest

from src.lib.Observable import Observer, Observable


class ObserverTestCase(unittest.TestCase):
    def mock_update(self, message, *args):
        return message == 'test'

    def setUp(self):
        self.observer = Observer()
        self.observer.update = self.mock_update

    def test_create(self):
        self.assertTrue(self.observer.is_ready)

    def test_update(self):

        self.assertTrue(self.observer.update('test'))

    def test_close_observer(self):
        self.observer.close_observer()
        self.assertFalse(self.observer.is_ready)


class ObservableTestCase(unittest.TestCase):
    def mock_update_1(self, message, *args):
        self.update_calls.append('{} 1'.format(message))

    def mock_update_2(self, message, *args):
        self.update_calls.append('{} 2'.format(message))

    def setUp(self):
        self.update_calls = []
        self.observable = Observable()
        self.observer1 = Observer()
        self.observer2 = Observer()
        self.observer1.update = self.mock_update_1
        self.observer2.update = self.mock_update_2

    def test_register(self):
        self.observable.register(self.observer1)
        self.assertEqual(len(self.observable.observers), 1)
        self.assertEqual(self.observable.observers, [self.observer1])

    def test_notify_one(self):
        notify_msg = ['1', '2', '3', '4']
        check_notify_msg = ['1 1', '2 1', '3 1', '4 1']
        self.observable.register(self.observer1)

        for msg in notify_msg:
            self.observable.notify(msg)
        self.assertEqual(self.update_calls, check_notify_msg)

    def test_notify_many(self):
        self.observable.register(self.observer1)
        self.observable.register(self.observer2)

        self.observable.notify('ok')
        self.assertEqual(self.update_calls, ['ok 1', 'ok 2'])

    def test_notify_when_closed(self):
        self.observable.register(self.observer1)
        self.observable.register(self.observer2)
        self.observer2.is_ready = False
        self.observable.notify('ok')
        self.assertEqual(self.update_calls, ['ok 1'])
