'''
A simple implementation of the CountMin data structure

Credit to:
https://github.com/rafacarrascosa/countminsketch/

on how the hash function is implemented
'''

from hashlib import md5


class CountMinSketch:
    """
    The countmin data structure
    """

    def __init__(self, depth, width, keep_true=False):
        self.depth = depth
        self.width = width
        self.matrix = [[0 for _ in range(width)] for _ in range(depth)]

    @classmethod
    def create_from_bounds(cls, eps, delta, keep_true=False):
        """
        Creates the data structure based on the eps and delta specified.
        """

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
        for row, index in zip(self.matrix, self.hash_item(new_item)):
            row[index] += value

    def count_item(self, item):
        """The estimated count of the item"""
        return min(row[index]
                   for row, index in zip(self.matrix, self.hash_item(item)))
