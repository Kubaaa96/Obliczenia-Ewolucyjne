import time

from PyQt6.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QLabel, QComboBox, QCheckBox, \
    QPushButton, QDialog
from PyQt6.QtCore import QPoint, QSize

from core.selection_methods import SelectionMethods
from core.cross_methods import CrossMethods
from core.mutation_methods import MutationMethods
from core.parameters import Parameters
from gui.utils.wrong_type_dialog import WrongTypeDialog
from gui.utils.elapsed_time_dialog import ElapsedTimeDialog
from genetics.genetic_algorithm import GeneticAlgorithm


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setup_window()
        self.begin_range_lineedit = QLineEdit()
        self.end_range_lineedit = QLineEdit()
        self.population_amount_lineedit = QLineEdit()
        self.number_of_bits_lineedit = QLineEdit()
        self.epochs_amount_lineedit = QLineEdit()
        self.best_tournament_amount_lineedit = QLineEdit()
        self.elite_amount_lineedit = QLineEdit()
        self.cross_prob_lineedit = QLineEdit()
        self.mutation_prob_lineedit = QLineEdit()
        self.inversion_prob_lineedit = QLineEdit()
        self.selection_combobox = QComboBox()
        self.cross_combobox = QComboBox()
        self.mutation_combobox = QComboBox()
        self.maximization_checkbox = QCheckBox("Maximization")

        self.not_valid_widgets = []

        self.init_gui()

    def setup_window(self):
        default_size = QSize(500, 700)

        self.resize(default_size)
        starting_location = QPoint(300, 100)
        self.move(starting_location)

        maximum_size = QSize(600, 800)
        self.setMaximumSize(maximum_size)

        minimum_size = QSize(300, 500)
        self.setMinimumSize(minimum_size)

        title = 'Obliczenia Ewolucyjne 1'
        self.setWindowTitle(title)

    def init_gui(self):
        main_layout = QVBoxLayout()
        # TODO insert function name insted of x
        main_label = QLabel("Genetic algorithm for finding max/min in x Function")
        main_label.setWordWrap(True)
        main_layout.addWidget(main_label)

        self.begin_range_lineedit.setPlaceholderText("Begin range")
        main_layout.addWidget(self.begin_range_lineedit)

        self.end_range_lineedit.setPlaceholderText("End range")
        main_layout.addWidget(self.end_range_lineedit)

        self.population_amount_lineedit.setPlaceholderText("Population amount")
        main_layout.addWidget(self.population_amount_lineedit)

        self.number_of_bits_lineedit.setPlaceholderText("Number of bits")
        main_layout.addWidget(self.number_of_bits_lineedit)

        self.epochs_amount_lineedit.setPlaceholderText("Epochs amount")
        main_layout.addWidget(self.epochs_amount_lineedit)

        self.best_tournament_amount_lineedit.setPlaceholderText("Best and tournament chromosome amount")
        main_layout.addWidget(self.best_tournament_amount_lineedit)

        self.elite_amount_lineedit.setPlaceholderText("Elite Strategy amount")
        main_layout.addWidget(self.elite_amount_lineedit)

        self.cross_prob_lineedit.setPlaceholderText("Cross probability")
        main_layout.addWidget(self.cross_prob_lineedit)

        self.mutation_prob_lineedit.setPlaceholderText("Mutation probability")
        main_layout.addWidget(self.mutation_prob_lineedit)

        self.inversion_prob_lineedit.setPlaceholderText("Inversion probability")
        main_layout.addWidget(self.inversion_prob_lineedit)

        selection_label = QLabel("Choose selection method")
        main_layout.addWidget(selection_label)

        self.selection_combobox.addItems(self.get_string_values_from(SelectionMethods))
        main_layout.addWidget(self.selection_combobox)

        cross_label = QLabel("Choose cross method")
        main_layout.addWidget(cross_label)

        self.cross_combobox.addItems(self.get_string_values_from(CrossMethods))
        main_layout.addWidget(self.cross_combobox)

        mutation_label = QLabel("Choose mutation method")
        main_layout.addWidget(mutation_label)

        self.mutation_combobox.addItems(self.get_string_values_from(MutationMethods))
        main_layout.addWidget(self.mutation_combobox)

        main_layout.addWidget(self.maximization_checkbox)

        start_pushbutton = QPushButton("Start")
        start_pushbutton.clicked.connect(self.clicked_start)
        main_layout.addWidget(start_pushbutton)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    @staticmethod
    def get_string_values_from(methods):
        return [str(method).split('.')[1] for method in methods]

    def clicked_start(self):
        parameters = self.validate_and_insert_widgets()

        if self.not_valid_widgets:
            dialog = WrongTypeDialog(self.not_valid_widgets)
            dialog.exec()
        else:
            genetic_algorithm = GeneticAlgorithm(parameters)
            start = time.time()
            genetic_algorithm.perform_operations()
            end = time.time()
            elapsed_time = end - start

            time_info_dialog = ElapsedTimeDialog(elapsed_time)
            time_info_dialog.exec()

            print(elapsed_time)

        self.not_valid_widgets.clear()

    def validate_and_insert_widgets(self) -> Parameters:
        parameters = Parameters()
        parameters.begin_range = self.validate_numbers(self.begin_range_lineedit, "Not numerical Begin Range Value", float)
        parameters.end_range = self.validate_numbers(self.end_range_lineedit, "Not Numerical End Range Value", float)
        parameters.population_amount = self.validate_numbers(self.population_amount_lineedit, "Not Numerical Population Amount Value", int)
        parameters.number_of_bits = self.validate_numbers(self.number_of_bits_lineedit, "Not Numerical Number of Bits Value", int)
        parameters.epochs_amount = self.validate_numbers(self.epochs_amount_lineedit, "Not Numerical Epochs Amount Value", int)
        parameters.best_tournament_amount = self.validate_numbers(self.best_tournament_amount_lineedit, "Not Numerical Best Tournament Amount Value", int)
        parameters.elite_amount = self.validate_numbers(self.elite_amount_lineedit, "Not Numerical Elite Amount Value", int)
        parameters.cross_prob = self.validate_probability(self.cross_prob_lineedit, "Not Numerical Cross Probability Value")
        parameters.mutation_prob = self.validate_probability(self.mutation_prob_lineedit, "Not Numerical Mutation Probability Value")
        parameters.inversion_prob = self.validate_probability(self.inversion_prob_lineedit, "Not Numerical Inversion Probability Value")
        parameters.selection_method = SelectionMethods(self.selection_combobox.currentIndex())
        parameters.cross_method = CrossMethods(self.cross_combobox.currentIndex())
        parameters.mutation_method = MutationMethods(self.mutation_combobox.currentIndex())
        parameters.maximization = self.maximization_checkbox.isChecked()
        self.validate_ranges(parameters.begin_range, parameters.end_range)
        return parameters

    def validate_numbers(self, lineedit, info_to_print_if_not_valid, data_type):
        try:
            value = data_type(lineedit.text())
            return value
        except ValueError as error:
            self.not_valid_widgets.append(info_to_print_if_not_valid + ": " + error.__str__())

    def validate_probability(self, lineedit, info_to_print_if_not_valid):
        try:
            value = float(lineedit.text())
            if 0 > value or value > 1:
                info_to_print_if_not_valid = info_to_print_if_not_valid.split(" ")[2]
                raise ValueError("Probability not from range [0,1]")
            return value
        except ValueError as error:
            self.not_valid_widgets.append(info_to_print_if_not_valid + ": " + error.__str__())

    def validate_ranges(self, begin_range, end_range):
        if begin_range >= end_range:
            self.not_valid_widgets.append("Wrong Ranges. Begin needs to be smaller than end")
