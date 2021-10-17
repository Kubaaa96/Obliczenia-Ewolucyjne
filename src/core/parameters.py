from core.selection_methods import SelectionMethods
from core.cross_methods import CrossMethods
from core.mutation_methods import MutationMethods


class Parameters:
    begin_range: int
    end_range: int
    population_amount: int
    number_of_bits: int
    epochs_amount: int
    best_tournament_amount: int
    elite_amount: int
    cross_prob: int
    mutation_prob: int
    inversion_prob: int
    selection_method: SelectionMethods
    cross_method: CrossMethods
    mutation_method: MutationMethods
    maximization: bool

    def __str__(self):
        return "Begin Range: " + str(self.begin_range) + "\n" + \
            "End Range: " + str(self.end_range) + "\n" + \
            "Population Amount: " + str(self.population_amount) + "\n" + \
            "Number of Bits: " + str(self.number_of_bits) + "\n" + \
            "Epochs Amount: " + str(self.epochs_amount) + "\n" + \
            "Best Tournament Amount: " + str(self.best_tournament_amount) + "\n" + \
            "Elite Amount: " + str(self.elite_amount) + "\n" + \
            "Cross Probability: " + str(self.cross_prob) + "\n" + \
            "Mutation Probability: " + str(self.mutation_prob) + "\n" + \
            "Inversion Probability: " + str(self.inversion_prob) + "\n" + \
            "Selection Method: " + str(self.selection_method) + "\n" + \
            "Cross Method: " + str(self.cross_method) + "\n" + \
            "Mutation Method: " + str(self.mutation_method) + "\n" + \
            "Maximization?: " + str(self.maximization) + "\n".format(self=self)
