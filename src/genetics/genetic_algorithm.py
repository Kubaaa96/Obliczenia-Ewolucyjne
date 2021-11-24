from genetics.population import Population
from genetics.chromosome import Chromosome
from genetics.individual import Individual
from core.parameters import Parameters
import matplotlib.pyplot as plt
import os


class GeneticAlgorithm:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def perform_operations(self):
        fitness_table = []
        epoch_table = []
        best_from_population = []
        best_temp = []
        obj = Population(self.parameters)
        obj.create_population()

        for x in range(self.parameters.population_amount):
            obj.save_results_to_txt_file('beggining_population_numbers', str(obj.population_list[x].x1.individual_decoded)+' '+str(obj.population_list[x].x2.individual_decoded)+'\n', x, self.parameters.population_amount)
        for epoch in range(self.parameters.epochs_amount):

            obj.selection()
            obj.cross()
            obj.mutation()
            obj.elite_strategy()
            obj.best_guy_from_epoch()
        # TODO Generate Diagrams
        # TODO save to DataBase or txt file
        for x in range(self.parameters.population_amount):
            obj.save_results_to_txt_file('final_results_numbers', str(obj.population_list[x].x1.individual_decoded)+' '+str(obj.population_list[x].x2.individual_decoded)+'\n', x, self.parameters.population_amount)
            obj.save_results_to_txt_file('best_from_epoch_numbers', str(obj.best_from_epoch[x].x1.individual_decoded)+ ' ' + str(obj.best_from_epoch[x].x2.individual_decoded) + '\n', x, self.parameters.population_amount)
            fitness_table.append(obj.population_list[x].f_x)
            epoch_table.append(x)
            best_temp.append([obj.population_list[x].f_x,x])
        best_temp.sort()
        print(best_temp)
        best_index_gen = int(best_temp[0][1])
        best_from_population_first = obj.population_list[best_index_gen].x1.individual_decoded
        best_from_population_second = obj.population_list[best_index_gen].x2.individual_decoded
        obj.save_results_to_txt_file('best_from_epoch_numbers', str(best_from_population_first)+' '+str(best_from_population_second))
        plt.plot(epoch_table, fitness_table)
        plt.xlabel('epoch')
        plt.ylabel('fitness function')
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
        plt.savefig(absolute_path+'\\graph.jpg')

