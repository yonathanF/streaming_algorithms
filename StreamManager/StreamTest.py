from unittest import TestCase, main
from Stream import SimpleStream
from random import randint

class SimpleStreamBasics(TestCase):
    def setUp(self):
        def random():
            x = randint(1, 1000)
            return x if x < 999 else None
        self.stream = SimpleStream(random)

    def tearDown(self):
        self.stream.shutdown()

    def test_subscribers_notified(self):
        def sub1(data):
            self.assertIsNotNone(data)
        def sub2(data):
            self.assertIsNotNone(data)

        self.stream.subscribe(sub1)
        self.stream.subscribe(sub2)


if __name__ == '__main__':
    main()
