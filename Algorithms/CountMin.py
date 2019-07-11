'''
A simple implementation of the CountMin data structure

Credit to:
https://github.com/rafacarrascosa/countminsketch/

on how the hash function is implemented
'''

import math
from collections import Counter
from hashlib import md5


class CountMinSketch:
    """
    The countmin data structure
    """

    def __init__(self, depth, width, keep_true=False):
        self.keep_true = keep_true
        self.complete_data = []
        self.depth = depth
        self.width = width
        self.matrix = [[0 for _ in range(width)] for _ in range(depth)]

    @classmethod
    def create_from_bounds(cls, eps, delta, keep_true=False):
        """
        Creates the data structure based on the eps and delta specified.
        """
        return cls(math.ceil(math.log((1 / delta), math.e)),
                   math.ceil(math.e / eps), keep_true)

    def get_true_freq(self):
        """If enabled, returns the true frequency of the data"""
        counts = Counter(self.complete_data)
        return sorted(counts.items(), key=lambda pair: pair[1], reverse=True)

    def hash_item(self, new_item):
        """
        Gets the column position for each row of the matrix

        .. note:: new_item must be hashable
        """
        md5_hash = md5(
            str(hash(str(new_item).encode('utf-8'))).encode('utf-8'))
        for row in range(self.depth):
            md5_hash.update(str(row).encode('utf-8'))
            yield int(md5_hash.hexdigest(), 16) % self.width

    def callback(self, data):
        """Subscription function for streams"""
        self.insert(data, 1)

    def insert(self, new_item, value):
        """Insert item into the countmin data structure"""
        if self.keep_true:
            self.complete_data.append((new_item, value))

        for row, index in zip(self.matrix, self.hash_item(new_item)):
            row[index] += value

    def count_item(self, item):
        """The estimated count of the item"""
        return min(row[index]
                   for row, index in zip(self.matrix, self.hash_item(item)))
