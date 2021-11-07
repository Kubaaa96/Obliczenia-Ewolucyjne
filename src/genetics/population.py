from core.parameters import Parameters
from genetics.individual import Individual
from core.selection_methods import SelectionMethods
from core.mutation_methods import MutationMethods
from core.cross_methods import CrossMethods
import random
import os


class Population:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.population_size = self.parameters.population_amount
        print(self.population_size)
        self.population_list = []
        self.prepared_to_crossing = []
        self.prepared_after_elite = []                                  # ELITE STRATEGY
        self.mutation_prob = self.parameters.mutation_prob              # MUTATION
        self.elite_amount = self.parameters.elite_amount                # MUTATION
        self.inversion_prob = self.parameters.inversion_prob
        self.crossover_prob = self.parameters.cross_prob

    def save_results_to_txt_file(self, file_name, data, current_range=0, end_range=0):
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
        full_path = absolute_path+'\\'+file_name+'.txt'
        if current_range == 0:
            if os.path.exists(full_path):
                os.remove(full_path)
            file = open(full_path, "a")
            file.write(str(data))
        else:
            file = open(full_path, "a+")
            file.write(str(data))
        if current_range == end_range:
            file.close()

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
        # print(temp_id)

        for i in temp_id:
            self.prepared_to_crossing.append(self.population_list[i])  # objects prepared for crossing

        # print(self.prepared_to_crossing[5].x1.individual_coded)
        # print(self.prepared_to_crossing[5].x2.individual_coded)

    def tournament_selection(self):
        number_of_tournament = int(self.parameters.best_tournament_amount / 100 * self.population_size)
        number_of_individual_in_group = int(self.population_size / number_of_tournament)

        samples = random.sample(range(self.population_size), self.population_size)
        # print(samples)

        temp = []

        for i in range(0, self.population_size, number_of_individual_in_group):
            temp_values = []
            for j in range(number_of_individual_in_group):
                temp_values.append(self.population_list[samples[i + j]].f_x)
            temp.append(temp_values)
        # print(temp)

        new_values = []

        for i in range(len(temp)):
            value = (min(temp[i], key=lambda v: abs(v - 0)))
            new_values.append(value)

        # print(new_values)

        id_values = []

        for i in new_values:
            for j in range(self.population_size):
                if self.population_list[j].f_x == i:
                    id_values.append(j)
        id_values.sort()
        # print(id_values)

        for i in id_values:
            self.prepared_to_crossing.append(self.population_list[i])  # objects prepared for crossing

        # print(self.prepared_to_crossing[5].x1.individual_coded)
        # print(self.prepared_to_crossing[5].x2.individual_coded)

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

            # print(result)

        else:
            for i in self.population_list:
                result += 1/i.f_x
            for i in range(0, self.population_size):
                probability_list.append((1/self.population_list[i].f_x) / result)

            distrib_list.append(probability_list[0])
            for i in range(1, self.population_size):
                distrib_list.append(distrib_list[i - 1] + probability_list[i])

            print(result)

        # for i in range(0, self.population_size):
            # print(distrib_list[i])

        rand_chance = random.uniform(0, 1)

        for i in range(0, self.population_size-1):
            if distrib_list[i] < rand_chance < distrib_list[i + 1]:
                self.prepared_to_crossing.append(self.population_list[i])
        # print(len(self.prepared_to_crossing))

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
        for elite_boy in range(0, self.elite_amount-1):
            self.prepared_after_elite.append(self.population_list[elite_boy])  # objects after elite strategy

    # ----------------------------------------------MUTATION----------------------------------------------
    # pobierane jest prepared_to_crossing z selekcji dlatego ze to jedyna tablica z osobnikami na ten moment.
    # powinna byc pobierana tablica z krzyzowania, ale jeszcze jej nie ma. zwracane tez jest prepared_to_crossing
    # tylko ze z podmienionymi osobnikami

    def one_point_mutation(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        rand_chance = random.uniform(0, 1)
        if self.mutation_prob <= rand_chance:
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                random_point = random.randint(0, bits)
                single_gen_list1 = list(single_gen1)
                single_gen_list2 = list(single_gen2)

                if single_gen_list1[random_point] == '1':
                    single_gen_list1[random_point] = '0'
                else:
                    single_gen_list1[random_point] = '1'
                if single_gen_list2[random_point] == '1':
                    single_gen_list2[random_point] = '0'
                else:
                    single_gen_list2[random_point] = '1'
                single_gen1 = ''.join(single_gen_list1)
                single_gen2 = ''.join(single_gen_list2)
                population[i].x1.individual_coded = single_gen1
                population[i].x2.individual_coded = single_gen2
            self.population_list = population

    def two_point_mutation(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        rand_chance = random.uniform(0, 1)
        if self.mutation_prob <= rand_chance:
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                random_point = random.randint(0, bits)
                random_point2 = random.randint(0, bits)
                while random_point == random_point2:
                    random_point2 = random.randint(0, bits)
                single_gen_list1 = list(single_gen1)
                single_gen_list2 = list(single_gen2)

                if single_gen_list1[random_point] == '1':
                    single_gen_list1[random_point] = '0'
                else:
                    single_gen_list1[random_point] = '1'
                if single_gen_list2[random_point] == '1':
                    single_gen_list2[random_point] = '0'
                else:
                    single_gen_list2[random_point] = '1'

                if single_gen_list1[random_point2] == '1':
                    single_gen_list1[random_point2] = '0'
                else:
                    single_gen_list1[random_point2] = '1'
                if single_gen_list2[random_point2] == '1':
                    single_gen_list2[random_point2] = '0'
                else:
                    single_gen_list2[random_point2] = '1'
                single_gen1 = ''.join(single_gen_list1)
                single_gen2 = ''.join(single_gen_list2)
                population[i].x1.individual_coded = single_gen1
                population[i].x2.individual_coded = single_gen2
            self.population_list = population

    def side_mutation(self):
        population = self.population_list
        rand_chance = random.uniform(0, 1)
        if self.mutation_prob <= rand_chance:
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                single_gen_list1 = list(single_gen1)
                single_gen_list2 = list(single_gen2)

                if single_gen_list1[-1] == '1':
                    single_gen_list1[-1] = '0'
                else:
                    single_gen_list1[-1] = '1'
                if single_gen_list2[-1] == '1':
                    single_gen_list2[-1] = '0'
                else:
                    single_gen_list2[-1] = '1'
                single_gen1 = ''.join(single_gen_list1)
                single_gen2 = ''.join(single_gen_list2)
                population[i].x1.individual_coded = single_gen1
                population[i].x2.individual_coded = single_gen2
            self.population_list = population

    def mutation(self):
        if self.parameters.mutation_method == MutationMethods.ONE_POINT:
            self.one_point_mutation()
        elif self.parameters.mutation_method == MutationMethods.TWO_POINT:
            self.two_point_mutation()
        else:
            self.side_mutation()

    def inversion(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        if bits > 1:
            first_point = random.randint(0, bits)
            second_point = random.randint(0, bits)
            while first_point == second_point:
                second_point = random.randint(0, bits)
            if first_point > second_point:
                for i in range(self.population_size):
                    single_gen = population[i].x1.individual_coded
                    rand_chance = random.uniform(0, 1)
                    if rand_chance <= self.inversion_prob:
                        reverse_point = int(first_point+1/2)
                        tempint = 0
                        for x in range(second_point, reverse_point):
                            single_gen_list = list(single_gen)
                            temp = single_gen_list[x]
                            single_gen_list[x] = single_gen_list[first_point - tempint]
                            single_gen_list[first_point-tempint] = temp
                            single_gen = ''.join(single_gen_list)
                            tempint = tempint + 1
                    population[i].x1.individual_coded = single_gen
                else:
                    for i in range(self.population_size):
                        single_gen = population[i].x2.individual_coded
                        rand_chance = random.uniform(0, 1)
                        if rand_chance <= self.inversion_prob:
                            reverse_point = int(second_point+1/2)
                            tempint = 0
                            for x in range(first_point, reverse_point):
                                single_gen_list = list(single_gen)
                                temp = single_gen_list[x]
                                single_gen_list[x] = single_gen_list[second_point-tempint]
                                single_gen_list[second_point-tempint] = temp
                                single_gen = ''.join(single_gen_list)
                                tempint = tempint + 1
                    population[i].x2.individual_coded = single_gen
        self.population_list = population

    def crossover_one_point(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        cross_point = random.randint(0, bits)
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            for i in range(self.population_size):
                single_gen = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                single_gen_list = list(single_gen)
                single_gen_list2 = list(single_gen2)
                for x in range(cross_point):
                    temp = single_gen_list[x]
                    single_gen_list[x] = single_gen_list2[x]
                    single_gen_list2[x] = temp
            single_gen = ''.join(single_gen_list)
            single_gen2 = ''.join(single_gen_list2)
            population[i].x1.individual_coded = single_gen
            population[i].x2.individual_coded = single_gen2
        self.population_list = population

    def crossover_two_point(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        cross_point = random.randint(0, bits)
        cross_point2 = random.randint(0, bits)
        while cross_point > cross_point2:
            cross_point = random.randint(0, bits)
            cross_point2 = random.randint(0, bits)
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            for i in range(self.population_size):
                single_gen = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                single_gen_list = list(single_gen)
                single_gen_list2 = list(single_gen2)
                for x in range(cross_point, cross_point2):
                    temp = single_gen_list[x]
                    single_gen_list[x] = single_gen_list2[x]
                    single_gen_list2[x] = temp
            single_gen = ''.join(single_gen_list)
            single_gen2 = ''.join(single_gen_list2)
            population[i].x1.individual_coded = single_gen
            population[i].x2.individual_coded = single_gen2
        self.population_list = population

    def crossover_three_point(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        cross_point = random.randint(0, bits - 2)
        cross_point2 = random.randint(0, bits - 1)
        cross_point3 = random.randint(0, bits)
        while cross_point > cross_point2 or cross_point2 > cross_point3:
            cross_point = random.randint(0, bits)
            cross_point2 = random.randint(0, bits)
            cross_point3 = random.randint(0, bits)
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            for i in range(self.population_size):
                single_gen = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                single_gen_list = list(single_gen)
                single_gen_list2 = list(single_gen2)
                for x in range(cross_point, cross_point2):
                    temp = single_gen_list[x]
                    single_gen_list[x] = single_gen_list2[x]
                    single_gen_list2[x] = temp
                for x in range(cross_point3, bits):
                    temp = single_gen_list[x]
                    single_gen_list[x] = single_gen_list2[x]
                    single_gen_list2[x] = temp
            single_gen = ''.join(single_gen_list)
            single_gen2 = ''.join(single_gen_list2)
            self.prepared_to_crossing.append([single_gen, single_gen2])
            population[i].x1.individual_coded = single_gen
            population[i].x2.individual_coded = single_gen2
        self.population_list = population

    def crossover_homogeneous(self):
        population = self.population_list
        bits = len(population[0].x1.individual_coded)
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            for i in range(self.population_size):
                single_gen = population[i].x1.individual_coded
                single_gen2 = population[i].x2.individual_coded
                single_gen_list = list(single_gen)
                single_gen_list2 = list(single_gen2)
                gen_list_temp = list(single_gen)
                gen_list_temp2 = list(single_gen2)
                for x in range(1, bits - 1, 2):
                    single_gen_list[x] = gen_list_temp2[x]
                for x in range(0, bits - 1, 2):
                    single_gen_list2[x] = gen_list_temp[x]
            single_gen = ''.join(single_gen_list)
            single_gen2 = ''.join(single_gen_list2)
            population[i].x1.individual_coded = single_gen
            population[i].x2.individual_coded = single_gen2
        self.population_list = population

    def cross(self):
        if self.parameters.cross_method == CrossMethods.ONE_POINT:
            self.crossover_one_point()
        elif self.parameters.cross_method == CrossMethods.TWO_POINT:
            self.crossover_two_point()
        elif self.parameters.cross_method == CrossMethods.THREE_POINTS:
            self.crossover_three_point()
        else:
            self.crossover_homogeneous()
