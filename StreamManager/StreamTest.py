from unittest import TestCase, main
from Stream import SimpleStream
from random import randint

class SumAlgorithm:
    def __init__(self):
        self.sum = 0

    def callback(self, data):
        self.sum += data

class CollectorAlgorithm:
    def __init__(self):
        self.items = []

    def callback(self, data):
        self.items.append(data)

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

    def test_subs_recieve_same_data(self):
       sub1 = SumAlgorithm()
       sub2 = CollectorAlgorithm()

       self.stream.subscribe(sub1.callback)
       self.stream.subscribe(sub2.callback)

       self.stream.shutdown()

       self.assertEqual(sub1.sum, sum(sub2.items))

if __name__ == '__main__':
    main()
