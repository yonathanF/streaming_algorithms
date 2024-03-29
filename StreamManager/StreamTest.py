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

class CollectorAlgorithm2(CollectorAlgorithm):
    pass

class DataSource:
    def __init__(self):
        self.count=0

    def data(self):
        self.count+=1
        return None if self.count > 1000 else self.count

class SimpleStreamCounterSource(TestCase):
    def setUp(self):
        self.source = DataSource()
        self.stream = SimpleStream(self.source.data)

    def test_subscribers_notified(self):
        def sub(data):
            self.assertIsNotNone(data)

        self.stream.subscribe(sub)

        self.stream.start()
        self.stream.shutdown()



class SimpleStreamBasics(TestCase):
    def setUp(self):
        def random():
            x = randint(1, 1000)
            return x if x < 999 else None
        self.stream = SimpleStream(random)

    def test_subscribers_notified(self):
        def sub1(data):
            self.assertIsNotNone(data)
        def sub2(data):
            self.assertIsNotNone(data)

        self.stream.subscribe(sub1)
        self.stream.subscribe(sub2)

        self.stream.start()
        self.stream.shutdown()

    def test_subs_recieve_same_data(self):
       sub1 = SumAlgorithm()
       sub2 = CollectorAlgorithm()
       sub3 = CollectorAlgorithm2()

       self.stream.subscribe(sub1.callback)
       self.stream.subscribe(sub2.callback)
       self.stream.subscribe(sub3.callback)

       self.stream.start()
       self.stream.shutdown()

       self.assertEqual(sub1.sum, sum(sub2.items))
       self.assertEqual(sub2.items.sort(), sub3.items.sort())

if __name__ == '__main__':
    main()
