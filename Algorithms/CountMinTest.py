"""
Test cases for the majority algorithm
"""

from unittest import TestCase, main

from Algorithms.CountMin import CountMinSketch
from StreamGen.BoundedStreams import BoundedBiasedRandom, BoundedRandom
from StreamManager.Stream import SimpleStream


class CountMinBasics(TestCase):
    def setUp(self):
        self.count_min = CountMinSketch(10, 10)
        # self.count_min_bound = CountMinSketch.create_from_bounds()

    def test_insert_unique(self):
        data = [i for i in range(10)]
        for item in data:
            self.count_min.insert(item, 1)

        for item in data:
            self.assertEqual(self.count_min.count_item(item), 1)

    def test_insert_dups(self):
        data = [i for i in range(10)]
        data_dups = [2, 2, 3, 3, 3]
        data.extend(data_dups)

        for item in data:
            self.count_min.insert(item, 1)

        self.assertEqual(self.count_min.count_item(2), 3)
        self.assertEqual(self.count_min.count_item(3), 4)

    def test_insert_dups_only(self):
        data = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        for item in data:
            self.count_min.insert(item, 1)

        self.assertEqual(self.count_min.count_item(1), 6)
        self.assertEqual(self.count_min.count_item(2), 4)

    def test_insert_twice_more(self):
        data = [i for i in range(20)]
        for item in data:
            self.count_min.insert(item, 1)

        for item in data:
            est = self.count_min.count_item(item)
            self.assertTrue((est in (1, 2)))

        self.assertTrue((self.count_min.count_item(1000) in (1, 0)))

    def test_insert_with_complete(self):
        count_min_complete = CountMinSketch(15, 15, True)
        data = [i for i in range(10)]
        data_dups = [2, 2, 3, 3, 3]
        data.extend(data_dups)

        for item in data:
            count_min_complete.insert(item, 1)

        for item in count_min_complete.get_true_freq():
            est = count_min_complete.count_item(item[0][0])
            self.assertEqual(item[1], est)

    def test_from_bounds(self):
        count_min = CountMinSketch.create_from_bounds(0.0001, 0.0000001)
        self.assertEqual(count_min.depth, 17)
        self.assertEqual(count_min.width, 27183)


class CountMinStreamIntegration(TestCase):
    def setUp(self):
        self.count_min = CountMinSketch(1000, 1000, True)
        self.source = BoundedRandom(1010, 1, 50)
        self.biased_source = BoundedBiasedRandom(1050, 1, 50, [1, 2, 3, 4], 90)
        self.stream = SimpleStream(self.source.gen_data)
        self.biased_stream = SimpleStream(self.biased_source.gen_data)

    def test_slightly_more_items_than_space(self):
        self.stream.subscribe(self.count_min.callback)
        self.stream.start()
        self.stream.shutdown()
        true_freq = self.count_min.get_true_freq()
        for value in true_freq:
            self.assertEqual(value[1], self.count_min.count_item(value[0][0]))

    def test_biased_data_large(self):
        self.biased_stream.subscribe(self.count_min.callback)
        self.biased_stream.start()
        self.biased_stream.shutdown()
        true_freq = self.count_min.get_true_freq()
        for value in true_freq:
            self.assertEqual(value[1], self.count_min.count_item(value[0][0]))


if __name__ == '__main__':
    main()
