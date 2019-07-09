"""
The Majority algorithm proposed by Demaine et al.

It's a generalization of the majority algorithm.
"""

import collections


class NoEmptyCounter(Exception):
    """The counters are full"""


class UnknownItem(Exception):
    """ A look up for an item that hasn't been seen before"""


class Majority:
    """
    Implements the M counter majority algorithm
    """

    def __init__(self, num_counters, keep_true_freq=False):

        # it's in a [item, freq] format
        self.counters = [[0, 0] for _ in range(num_counters)]
        self.keep_true_freq = keep_true_freq
        if keep_true_freq:
            self.complete_list = []

    def get_frequent_items(self):
        """Most frequent elements"""
        return sorted(self.counters, key=lambda pair: pair[1], reverse=True)

    def get_true_freq(self):
        """If enabled, returns the true frequency of the data"""
        counts = collections.Counter(self.complete_list)
        return sorted(counts.items(), key=lambda pair: pair[1], reverse=True)

    def is_monitored(self, element):
        """ Checks if the element is monitored by some counter"""
        for index, monitored_el in enumerate(self.counters):
            if monitored_el[0] == element:
                return index

        raise UnknownItem("Item not monitored.")

    def find_zero_counter(self):
        """Tries to find an empty counter"""
        for index, monitored_el in enumerate(self.counters):
            if monitored_el[1] == 0:
                return index

        raise NoEmptyCounter("No empty counters.")

    def decrement_all(self):
        """Decrements all the counters"""
        for monitored_el in self.counters:
            if monitored_el[1] > 0:
                monitored_el[1] -= 1

    def callback(self, data):
        """
        Subscription to data source
        :param data: must be hashable
        """
        self.insert_data(data)

    def insert_data(self, data):
        """Inserts a new data point according to the algorithm"""
        if self.keep_true_freq:
            self.complete_list.append(data)

        try:
            index = self.is_monitored(data)
            self.counters[index][1] += 1

        except UnknownItem:
            try:
                empty_index = self.find_zero_counter()
                self.counters[empty_index] = [data, 1]

            except NoEmptyCounter:
                self.decrement_all()
