from core.parameters import Parameters
import math as mth
import random


class Chromosome:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.a = self.parameters.begin_range
        self.b = self.parameters.end_range
        self.m = self.parameters.number_of_bits
        self.m_length = self.m_length()

        self.individual_coded = self.random_binary()
        self.individual_decoded = self.decode_x()

    def m_length(self):
        return mth.ceil(mth.log2((self.b - self.a) * pow(10, self.m)))

    def random_binary(self):
        c = ""
        for _ in range(self.m_length):
            temp = random.randint(0, 1)
            c += str(temp)
        return c

    def decode_x(self):
        return self.a + int(self.individual_coded, 2) * (self.b - self.a) / (pow(2, self.m_length) - 1)
