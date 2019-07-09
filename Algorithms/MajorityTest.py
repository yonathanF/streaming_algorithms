"""
Test cases for the majority algorithm
"""

from unittest import TestCase, main

from Algorithms.Majority import Majority

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


if __name__ == '__main__':
    main()
