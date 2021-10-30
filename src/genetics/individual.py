from core.parameters import Parameters
from genetics.chromosome import Chromosome


class Individual:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.x1 = Chromosome(self.parameters)
        self.x2 = Chromosome(self.parameters)
        self.f_x = self.fitness_func()

    def fitness_func(self):
        return (1.5 - self.x1.individual_decoded + self.x1.individual_decoded * self.x1.individual_decoded)**2 + (2.25 - self.x1.individual_decoded + self.x1.individual_decoded * self.x1.individual_decoded**2)**2 + (6.625 - self.x1.individual_decoded + self.x1.individual_decoded * self.x1.individual_decoded**3)**2
