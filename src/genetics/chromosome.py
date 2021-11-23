from core.parameters import Parameters
import math as mth
import numpy as np


class Chromosome:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.a = self.parameters.begin_range
        self.b = self.parameters.end_range
        self.individual_decoded = self.random_value()

    def random_value(self):
        return np.random.uniform(self.a, self.b, 1)
