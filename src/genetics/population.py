from core.parameters import Parameters
from genetics.individual import Individual
from core.selection_methods import SelectionMethods
from core.mutation_methods import MutationMethods
from core.cross_methods import CrossMethods
import random
import numpy as np
import os


class Population:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters
        self.population_size = self.parameters.population_amount
        print(self.population_size)
        self.population_list = []
        self.prepared_to_crossing = []
        self.prepared_after_elite = []                                  # ELITE STRATEGY
        self.best_from_epoch = []
        self.mutation_prob = self.parameters.mutation_prob              # MUTATION
        self.elite_amount = self.parameters.elite_amount                # MUTATION
        self.crossover_prob = self.parameters.cross_prob
        self.a = self.parameters.begin_range
        self.b = self.parameters.end_range

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
        number_of_tournament = int(round(self.parameters.best_tournament_amount / 100 * self.population_size))
        number_of_individual_in_group = int(round(self.population_size / number_of_tournament))

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

            #print(result)

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


    def mutation_uniform(self):
        population = self.population_list
        mutation_chance = random.uniform(0, 1)
        if self.mutation_prob <= mutation_chance:
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_decoded
                single_gen2 = population[i].x2.individual_decoded
                gen_chance = random.randint(0, 1)
                if gen_chance == 0:
                    single_gen1 = random.randint(int(self.a), int(self.b))
                else:
                    single_gen2 = random.randint(int(self.a), int(self.b))

                population[i].x1.individual_decoded = single_gen1
                population[i].x2.individual_decoded = single_gen2
            self.population_list = population

    def mutation_index_swap(self):
        population = self.population_list
        mutation_chance = random.uniform(0, 1)
        if self.mutation_prob <= mutation_chance:
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_decoded
                single_gen2 = population[i].x2.individual_decoded
                temp = single_gen1
                single_gen1 = single_gen2
                single_gen2 = temp

                population[i].x1.individual_decoded = single_gen1
                population[i].x2.individual_decoded = single_gen2
            self.population_list = population

    def mutation_gauss(self):
        population = self.population_list
        mutation_chance = random.uniform(0, 1)
        if self.mutation_prob <= mutation_chance:
            gauss = np.random.normal(0, 1)
            for i in range(self.population_size):
                single_gen1 = population[i].x1.individual_decoded
                single_gen2 = population[i].x2.individual_decoded
                gaussian_single_gen1 = float(single_gen1 + gauss)
                gaussian_single_gen2 = float(single_gen2 + gauss)
                while gaussian_single_gen1 > self.b or gaussian_single_gen1 < self.a:
                    gauss = np.random.normal(0, 1)
                    gaussian_single_gen1 = float(single_gen1 + gauss)
                while gaussian_single_gen2 > self.b or gaussian_single_gen2 < self.a:
                    gauss = np.random.normal(0, 1)
                    gaussian_single_gen2 = float(single_gen2 + gauss)
                single_gen1 = gaussian_single_gen1
                single_gen2 = gaussian_single_gen2

                population[i].x1.individual_decoded = single_gen1
                population[i].x2.individual_decoded = single_gen2
            self.population_list = population

    def mutation(self):
        if self.parameters.mutation_method == MutationMethods.Uniform:
            self.mutation_uniform()
        elif self.parameters.mutation_method == MutationMethods.IndexSwap:
            self.mutation_index_swap()
        else:
            self.mutation_gauss()

    def crossover_arithemtic(self):
        population = self.population_list
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            k_param = random.uniform(0, 1)
            for i in range(0,self.population_size,2):
                x1 = population[i].x1.individual_decoded
                y1 = population[i].x2.individual_decoded
                if i < self.population_size:
                    x2 = population[i+1].x1.individual_decoded
                    y2 = population[i+1].x2.individual_decoded
                else:
                    x2 = population[0].x1.individual_decoded
                    y2 = population[0].x2.individual_decoded
                x1_new = k_param * x1 + (1-k_param) * x2
                y1_new = k_param * y1 + (1-k_param) * y2
                x2_new = (1-k_param) * x1 + k_param * x2
                y2_new = (1-k_param) * y1 + k_param * y2
                #print(str(x1_new)+' '+str(y1_new)+' '+str(x2_new)+' '+str(y2_new))
                population[i].x1.individual_decoded = x1_new
                population[i].x2.individual_decoded = y1_new
                if i < self.population_size:
                    population[i+1].x1.individual_decoded = x2_new
                    population[i+1].x2.individual_decoded = y2_new
                else:
                    population[0].x1.individual_decoded = x2_new
                    population[0].x2.individual_decoded = y2_new
            self.population_list = population

    def crossover_heuristic(self):
        population = self.population_list
        rand_chance = random.uniform(0, 1)
        if rand_chance <= self.crossover_prob:
            k_param = random.uniform(0, 1)
            for i in range(self.population_size):
                x1 = population[i].x1.individual_decoded
                y1 = population[i].x2.individual_decoded
                random_choose = random.randint(0, self.population_size-1)
                x2 = population[random_choose].x1.individual_decoded
                y2 = population[random_choose].x2.individual_decoded
                while x1>x2 and y1>y2:
                    random_choose = random.randint(0, self.population_size-1)
                    x2 = population[random_choose].x1.individual_decoded
                    y2 = population[random_choose].x2.individual_decoded
                x1_new = k_param * (x2-x1) + x1
                y1_new = k_param * (y2-y1) + y1
                #print(str(x1_new)+' '+str(y1_new))
                population[i].x1.individual_decoded = x1_new
                population[i].x2.individual_decoded = y1_new
            self.population_list = population

    def cross(self):
        if self.parameters.cross_method == CrossMethods.Arithmetic:
            self.crossover_arithemtic()
        else:
            self.crossover_heuristic()

    def best_guy_from_epoch(self):
        fitness_list = []
        sorted_fitness = []
        best_guy = self.best_from_epoch
        population = self.population_list

        for i in range(len(population)-1):
            fitness_list.append(population[i].f_x)
            sorted_fitness.append(fitness_list[i])
        sorted_fitness.sort()

        for j in range(len(fitness_list)-1):
            if fitness_list[j] == sorted_fitness[0]:
                best_guy.append(population[j])

        self.best_from_epoch = best_guy

        #print("best", self.best_from_epoch)
        #print('fitness', fitness_list)
        #print('sorted', sorted_fitness)

