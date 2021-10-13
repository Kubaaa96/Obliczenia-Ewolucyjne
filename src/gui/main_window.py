from PyQt6.QtWidgets import QMainWindow, QWidget, QLineEdit, QVBoxLayout, QLabel, QComboBox, QCheckBox, \
    QPushButton
from PyQt6.QtCore import QPoint, QSize


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

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

        self.init_gui()

    def init_gui(self):
        main_layout = QVBoxLayout()
        # TODO insert function name insted of x
        main_label = QLabel("Genetic algorithm for finding max/min in x Function")
        main_label.setWordWrap(True)
        main_layout.addWidget(main_label)

        begin_range_lineedit = QLineEdit()
        begin_range_lineedit.setPlaceholderText("Begin range")
        main_layout.addWidget(begin_range_lineedit)

        end_range_lineedit = QLineEdit()
        end_range_lineedit.setPlaceholderText("End range")
        main_layout.addWidget(end_range_lineedit)

        population_amount_lineedit = QLineEdit()
        population_amount_lineedit.setPlaceholderText("Population amount")
        main_layout.addWidget(population_amount_lineedit)

        number_of_bits_lineedit = QLineEdit()
        number_of_bits_lineedit.setPlaceholderText("Number of bits")
        main_layout.addWidget(number_of_bits_lineedit)

        epochs_amount_lineedit = QLineEdit()
        epochs_amount_lineedit.setPlaceholderText("Epochs amount")
        main_layout.addWidget(epochs_amount_lineedit)

        best_tournament_amount_lineedit = QLineEdit()
        best_tournament_amount_lineedit.setPlaceholderText("Best and tournament chromosome amount")
        main_layout.addWidget(best_tournament_amount_lineedit)

        elite_amount_lineedit = QLineEdit()
        elite_amount_lineedit.setPlaceholderText("Elite Strategy amount")
        main_layout.addWidget(elite_amount_lineedit)

        cross_prob_lineedit = QLineEdit()
        cross_prob_lineedit.setPlaceholderText("Cross probability")
        main_layout.addWidget(cross_prob_lineedit)

        mutation_prob_lineedit = QLineEdit()
        mutation_prob_lineedit.setPlaceholderText("Mutation probability")
        main_layout.addWidget(mutation_prob_lineedit)

        inversion_prob_lineedit = QLineEdit()
        inversion_prob_lineedit.setPlaceholderText("Inversion probability")
        main_layout.addWidget(inversion_prob_lineedit)

        selection_label = QLabel("Choose selection method")
        main_layout.addWidget(selection_label)

        selection_combobox = QComboBox()
        selection_combobox.addItems(["BEST", "ROULETTE", "TOURNAMENT"])
        main_layout.addWidget(selection_combobox)

        cross_label = QLabel("Choose cross method")
        main_layout.addWidget(cross_label)

        cross_combobox = QComboBox()
        cross_combobox.addItems(["One Point", "Two points", "Three points", "Homo"])
        main_layout.addWidget(cross_combobox)

        mutation_label = QLabel("Choose mutation method")
        main_layout.addWidget(mutation_label)

        mutation_combobox = QComboBox()
        mutation_combobox.addItems(["One Point", "Two Points"])
        main_layout.addWidget(mutation_combobox)

        maximization_checkbox = QCheckBox("Maximization")
        main_layout.addWidget(maximization_checkbox)

        start_pushbutton = QPushButton("Start")
        main_layout.addWidget(start_pushbutton)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

