from core.parameters import Parameters
from genetics.individual import Individual
import random


class Population:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.population_size = self.parameters.population_amount
        print(self.population_size)
        self.population_list = []
        self.prepared_to_crossing = []

    def create_population(self):
        for _ in range(self.population_size):
            self.population_list.append(Individual(self.parameters))
            #print(self.population_list[_].x1.individual_coded)
            #print(self.population_list[_].x1.individual_decoded)
            #print(self.population_list[_].f_x)

    def best_selection(self):
        chance_to_rand = int(self.parameters.best_tournament_amount / 100 * self.population_size)

        sorted_list = []
        temp_id = []

        for _ in range(self.population_size):
            sorted_list.append(self.population_list[_].f_x)
        sorted_list.sort()
        for i in range(int(chance_to_rand)):
            value = (min(sorted_list, key=lambda v: abs(v - 0)))
            for j in range(self.population_size):
                if self.population_list[j].f_x == value:
                    temp_id.append(j)
                    sorted_list.remove(value)
        temp_id.sort()
        print(temp_id)

        for i in temp_id:
            self.prepared_to_crossing.append(self.population_list[i]) #objects prepared for crossing

        #print(self.prepared_to_crossing[5])

    def tournament_selection(self):
        number_of_tournament = int(self.parameters.best_tournament_amount / 100 * self.population_size)
        number_of_individual_in_group = int(self.population_size / number_of_tournament)

        samples = random.sample(range(self.population_size), self.population_size)
        print(samples)

        temp = []

        for i in range(0, self.population_size, number_of_individual_in_group):
            temp_values = []
            for j in range(number_of_individual_in_group):
                temp_values.append(self.population_list[samples[i + j]].f_x)
            temp.append(temp_values)
        print(temp)

        new_values = []

        for i in range(len(temp)):
            value = (min(temp[i], key=lambda v: abs(v - 0)))
            new_values.append(value)

        print(new_values)

        id_values = []

        for i in new_values:
            for j in range(self.population_size):
                if self.population_list[j].f_x == i:
                    id_values.append(j)
        id_values.sort()
        print(id_values)

        for i in id_values:
            self.prepared_to_crossing.append(self.population_list[i]) #objects prepared for crossing

        #print(self.prepared_to_crossing[5])

    # TODO roulette_selection() -> deleted due to issue in implementation
    # New solution in progress