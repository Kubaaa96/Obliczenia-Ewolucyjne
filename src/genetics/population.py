from core.parameters import Parameters
from genetics.individual import Individual
from core.selection_methods import SelectionMethods
from core.mutation_methods import MutationMethods
import random


class Population:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.population_size = self.parameters.population_amount
        print(self.population_size)
        self.population_list = []
        self.prepared_to_crossing = []
        self.mutation_prob = self.parameters.mutation_prob              # MUTATION
        self.num_of_bits = self.parameters.number_of_bits               # MUTATION
        self.elite_amount = self.parameters.elite_amount                # MUTATION
        self.prepared_after_elite = []                                  # ELITE STRATEGY

    def create_population(self):
        for _ in range(self.population_size):
            self.population_list.append(Individual(self.parameters))

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
        #print(temp_id)

        for i in temp_id:
            self.prepared_to_crossing.append(self.population_list[i]) #objects prepared for crossing

        #print(self.prepared_to_crossing[5].x1.individual_coded)
        #print(self.prepared_to_crossing[5].x2.individual_coded)

    def tournament_selection(self):
        number_of_tournament = int(self.parameters.best_tournament_amount / 100 * self.population_size)
        number_of_individual_in_group = int(self.population_size / number_of_tournament)

        samples = random.sample(range(self.population_size), self.population_size)
        #print(samples)

        temp = []

        for i in range(0, self.population_size, number_of_individual_in_group):
            temp_values = []
            for j in range(number_of_individual_in_group):
                temp_values.append(self.population_list[samples[i + j]].f_x)
            temp.append(temp_values)
        #print(temp)

        new_values = []

        for i in range(len(temp)):
            value = (min(temp[i], key=lambda v: abs(v - 0)))
            new_values.append(value)

        #print(new_values)

        id_values = []

        for i in new_values:
            for j in range(self.population_size):
                if self.population_list[j].f_x == i:
                    id_values.append(j)
        id_values.sort()
        #print(id_values)

        for i in id_values:
            self.prepared_to_crossing.append(self.population_list[i]) #objects prepared for crossing

        #print(self.prepared_to_crossing[5].x1.individual_coded)
        #print(self.prepared_to_crossing[5].x2.individual_coded)

    def roulette_selection(self):
        result = 0.0
        probability_list = []
        distrib_list = []

        if self.parameters.maximization:
            for i in self.population_list:
                result += i.f_x
            for i in range(0, self.population_size):
                probability_list.append(self.population_list[i].f_x/result)

            distrib_list.append(probability_list[0])
            for i in range(1, self.population_size):
                distrib_list.append(distrib_list[i-1] + probability_list[i])

            #print(result)

        else:
            for i in self.population_list:
                result += 1/i.f_x
            for i in range(0, self.population_size):
                probability_list.append((1/self.population_list[i].f_x) / result)

            distrib_list.append(probability_list[0])
            for i in range(1, self.population_size):
                distrib_list.append(distrib_list[i - 1] + probability_list[i])

            print(result)

        #for i in range(0, self.population_size):
            #print(distrib_list[i])

        rand_chance = random.uniform(0, 1)

        for i in range(0, self.population_size-1):
            if distrib_list[i] < rand_chance < distrib_list[i + 1]:
                self.prepared_to_crossing.append(self.population_list[i])
        #print(len(self.prepared_to_crossing))

    def selection(self):
        if self.parameters.selection_method == SelectionMethods.BEST:
            self.best_selection()
        elif self.parameters.selection_method == SelectionMethods.ROULETTE:
            self.roulette_selection()
        else:
            self.tournament_selection()

    # -----------------------------------------------ELITE-----------------------------------------------
    # prepared_after_elite to tablica ktora ma osobnikow wybranych z elitarnej strategii
    # na samym koncu trzeba ja dopisac do listy z osobnikami po wszystkich przejsciach
    #

    def elite_strategy(self):
        for elite_boy in range(0, self.elite_amount):
            self.prepared_after_elite.append(self.prepared_to_crossing[elite_boy])  # objects after elite strategy

    # ----------------------------------------------MUTATION----------------------------------------------
    # pobierane jest prepared_to_crossing z selekcji dlatego ze to jedyna tablica z osobnikami na ten moment.
    # powinna byc pobierana tablica z krzyzowania, ale jeszcze jej nie ma. zwracane tez jest prepared_to_crossing
    # tylko ze z podmienionymi osobnikami

    def one_point_mutation(self):
        for i in range(len(self.prepared_to_crossing[self.elite_amount:])):
            rand_chance = random.uniform(0, 1)

            if self.mutation_prob <= rand_chance:
                x1 = self.prepared_to_crossing[i].x1.individual_coded
                x2 = self.prepared_to_crossing[i].x2.individual_coded

                random_point = random.randint(0, len(x1))
                if x1[random_point] == '0':
                    x1 = x1[:random_point] + '1' + x1[random_point+1:]
                else:
                    x1 = x1[:random_point] + '0' + x1[random_point+1:]

                if x2[random_point] == '0':
                    x2 = x2[:random_point] + '1' + x2[random_point+1:]
                else:
                    x2 = x2[:random_point] + '0' + x2[random_point+1:]

                x1 = self.prepared_to_crossing[i].x1.individual_decoded
                x2 = self.prepared_to_crossing[i].x2.individual_decoded
                self.prepared_to_crossing[i] = x1, x2
                print("asa", self.prepared_to_crossing)

    def two_point_mutation(self):
        for i in range(len(self.prepared_to_crossing[self.elite_amount:])):
            rand_chance = random.uniform(0, 1)

            if self.mutation_prob <= rand_chance:
                x1 = self.prepared_to_crossing[i].x1.individual_coded
                x2 = self.prepared_to_crossing[i].x2.individual_coded

                random_point1 = random.randint(0, len(x1))
                random_point2 = random.randint(0, len(x1))
                while random_point1 == random_point2:
                    random_point2 = random.randint(0, len(x1))

                if x1[random_point1] == '0':
                    x1 = x1[:random_point1] + '1' + x1[random_point1 + 1:]
                else:
                    x1 = x1[:random_point1] + '0' + x1[random_point1 + 1:]

                if x1[random_point2] == '0':
                    x1 = x1[:random_point2] + '1' + x1[random_point2 + 1:]
                else:
                    x1 = x1[:random_point2] + '0' + x1[random_point2 + 1:]

                if x2[random_point1] == '0':
                    x2 = x2[:random_point1] + '1' + x2[random_point1 + 1:]
                else:
                    x2 = x2[:random_point1] + '0' + x2[random_point1 + 1:]

                if x2[random_point2] == '0':
                    x2 = x2[:random_point2] + '1' + x2[random_point2 + 1:]
                else:
                    x2 = x2[:random_point2] + '0' + x2[random_point2 + 1:]

                x1 = self.prepared_to_crossing[i].x1.individual_decoded
                x2 = self.prepared_to_crossing[i].x2.individual_decoded

                self.prepared_to_crossing[i] = x1, x2

    def side_mutation(self):
        for i in range(len(self.prepared_to_crossing[self.elite_amount:])):
            rand_chance = random.uniform(0, 1)

            if self.mutation_prob <= rand_chance:
                x1 = self.prepared_to_crossing[i].x1.individual_coded
                x2 = self.prepared_to_crossing[i].x2.individual_coded

                if x1[-1] == '0':
                    x1 = x1[:-1] + '1'
                else:
                    x1 = x1[:-1] + '0'

                if x2[-1] == '0':
                    x2 = x1[:-1] + '1'
                else:
                    x2 = x1[:-1] + '0'

                x1 = self.prepared_to_crossing[i].x1.individual_decoded
                x2 = self.prepared_to_crossing[i].x2.individual_decoded
                self.prepared_to_crossing[i] = x1, x2

    def mutation(self):
        if self.parameters.mutation_method == MutationMethods.ONE_POINT:
            self.one_point_mutation()
        elif self.parameters.mutation_method == MutationMethods.TWO_POINT:
            self.two_point_mutation()
        else:
            self.side_mutation()
