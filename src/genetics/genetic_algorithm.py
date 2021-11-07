from genetics.population import Population
from genetics.chromosome import Chromosome
from genetics.individual import Individual
from core.parameters import Parameters


class GeneticAlgorithm:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def perform_operations(self):
        print(self.parameters)  # Temp

        obj = Population(self.parameters)
        obj.create_population()

        for epoch in range(self.parameters.epochs_amount):
            print(f'\nStart of epoch {epoch}')
            # TODO Evaluation
            # TODO Selection
            obj.selection()
            # TODO Crossover
            obj.cross()
            # TODO Mutation
            obj.mutation()
            # TODO Inversion
            obj.inversion()
            # TODO Elite Strategy
            obj.elite_strategy()
        # TODO Generate Diagrams
        # TODO save to DataBase or txt file
        for x in range(self.parameters.population_amount):
            obj.save_results_to_txt_file('final_results', obj.population_list[x].x1.individual_coded+' '+obj.population_list[x].x2.individual_coded+'\n', x, self.parameters.population_amount)