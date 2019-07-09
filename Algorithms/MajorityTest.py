"""
Test cases for the majority algorithm
"""

from time import sleep
from unittest import TestCase, main

from Algorithms.Majority import Majority, NoEmptyCounter, UnknownItem
from StreamGen.BoundedStreams import BoundedBiasedRandom, BoundedRandom
from StreamManager.Stream import SimpleStream


class MajorityBasics(TestCase):
    def setUp(self):
        self.majority = Majority(10)

    def test_unknown_insert_empty_unique(self):
        for data in range(10):
            self.majority.insert_data(data)
            self.assertIn([data, 1], self.majority.counters)

    def test_unknown_insert_empty_dups(self):
        for _ in range(5):
            for data in range(10):
                self.majority.insert_data(data)

        for data in range(10):
            self.assertIn([data, 5], self.majority.counters)

    def test_no_counter_found(self):
        for data in range(10):
            self.majority.insert_data(data)

        with self.assertRaises(NoEmptyCounter):
            self.majority.find_zero_counter()

    def test_find_unknown(self):
        with self.assertRaises(UnknownItem):
            self.majority.is_monitored(999)

    def test_keep_true(self):
        majority = Majority(10, True)
        data = [1, 2, 3, 3, 3, 3, 1, 1, 9, 9]
        for value in data:
            majority.insert_data(value)

        expected = [(3, 4), (1, 3), (9, 2), (2, 1)]
        self.assertEqual(expected, majority.get_true_freq())

    def test_correct_when_enough_counters(self):
        majority = Majority(4, True)
        data = [1, 2, 3, 3, 3, 3, 1, 1, 9, 9]
        for value in data:
            majority.insert_data(value)

        true_freq = majority.get_true_freq()
        for item in majority.counters:
            self.assertIn(tuple(item), true_freq)


class MajorityStreamIntegration(TestCase):
    def setUp(self):
        self.majority = Majority(10, True)
        self.source = BoundedRandom(55, 1, 50)
        self.biased_source = BoundedBiasedRandom(55, 1, 50, [1, 2, 3, 4], 90)
        self.stream = SimpleStream(self.source.gen_data)
        self.biased_stream = SimpleStream(self.biased_source.gen_data)

    def test_stream_source_connect(self):
        def simple_ping(data):
            self.assertGreater(data, 0)
            self.assertLess(data, 51)

        self.stream.subscribe(simple_ping)
        self.stream.start()
        self.stream.shutdown()

    def test_stream_source_majority(self):
        self.biased_stream.subscribe(self.majority.callback)
        self.biased_stream.start()
        sleep(0.1)
        self.biased_stream.shutdown()

        true_freq = self.majority.get_true_freq()[:10]
        true_freq_filtered = []
        for item in true_freq:
            true_freq_filtered.append(item[0])

        counter_filtered = []
        for item in self.majority.counters:
            counter_filtered.append(item[0])

        for item in true_freq_filtered:
            self.assertIn(item, counter_filtered)


if __name__ == '__main__':
    main()
