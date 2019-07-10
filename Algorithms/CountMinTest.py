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

        self.assertEqual(self.count_min.count_item(100), 0)


class CountMinStreamIntegration(TestCase):
    def setUp(self):
        self.count_min = CountMinSketch(10, 10)
        self.source = BoundedRandom(55, 1, 50)
        self.biased_source = BoundedBiasedRandom(55, 1, 50, [1, 2, 3, 4], 90)
        self.stream = SimpleStream(self.source.gen_data)
        self.biased_stream = SimpleStream(self.biased_source.gen_data)


if __name__ == '__main__':
    main()
