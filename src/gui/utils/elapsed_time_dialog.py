from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt


class ElapsedTimeDialog(QDialog):
    def __init__(self, time):
        super(ElapsedTimeDialog, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        title = "Elapsed TIme"
        self.setWindowTitle(title)

        self.main_layout = QVBoxLayout()

        self.message = "Time passed: " + str(time) + " seconds"

        self.message_label = QLabel(self.message)
        self.main_layout.addWidget(self.message_label)

        buttons = QDialogButtonBox.StandardButton.Ok
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)

        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

