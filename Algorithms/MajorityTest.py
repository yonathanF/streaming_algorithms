"""
Test cases for the majority algorithm
"""

from unittest import TestCase, main

from Algorithms.Majority import Majority, NoEmptyCounter, UnknownItem

# from StreamManager.Stream import SimpleStream


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

        expected = {3: 4, 1: 3, 9: 2, 2: 1}
        self.assertEqual(expected, majority.get_true_freq())


if __name__ == '__main__':
    main()
