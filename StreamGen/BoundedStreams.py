"""
A set of finite streams where the bound can be passed as a parameter
"""

from random import choice, randint


class BoundedRandom:
    """A finite stream of random integers within a limited range"""

    def __init__(self, count_limit, range_low, range_high):
        self.count = 0
        self.count_limit = count_limit
        self.range_low = range_low
        self.range_high = range_high

    def gen_data(self):
        """Generate the data as expected"""
        self.count += 1
        return None if self.count > self.count_limit else randint(
            self.range_low, self.range_high)


class BoundedBiasedRandom(BoundedRandom):
    """
    Extends the basic finite stream by letting the user specify
    values more favored out of the range
    """

    def __init__(self, count_limit, range_low, range_high, favored_values,
                 bias):
        super().__init__(count_limit, range_low, range_high)
        self.favored = favored_values
        self.bias = bias

    def gen_data(self):
        data = super().gen_data()
        if data:
            random_choice = randint(0, 100)
            return data if random_choice > self.bias else choice(self.favored)

        return None
