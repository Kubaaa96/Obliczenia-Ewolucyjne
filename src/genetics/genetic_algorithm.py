from genetics.population import Population
from genetics.chromosome import Chromosome
from genetics.individual import Individual
from core.parameters import Parameters


class GeneticAlgorithm:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def perform_operations(self):
        print(self.parameters) # Temp

        obj = Population(self.parameters)
        obj.create_population()

        for epoch in range(self.parameters.epochs_amount):
            print(f'\nStart of epoch {epoch}')
            obj.selection()
            obj.mutation()
            # TODO Evaluation
            # TODO Selection
            # TODO Crossover
            # TODO Mutation
            # TODO Inversion
            # TODO Elite Strategy

        # TODO Generate Diagrams
        # TODO save to DataBase or txt file
