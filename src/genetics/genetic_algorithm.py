from core.parameters import Parameters

class GeneticAlgorithm:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

    def perform_operations(self):
        print(self.parameters) # Temp
        # TODO Initialize Population
        for epoch in range(self.parameters.epochs_amount):
            print(f'\nStart of epoch {epoch}')
            # TODO Evaluation
            # TODO Selection
            # TODO Crossover
            # TODO Mutation
            # TODO Inversion
            # TODO Elite Strategy

        # TODO Generate Diagrams
        # TODO save to DataBase or txt file

