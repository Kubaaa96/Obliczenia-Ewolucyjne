from PyQt6.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox
from PyQt6.QtCore import Qt


class WrongTypeDialog(QDialog):
    def __init__(self, contents):
        super(WrongTypeDialog, self).__init__()

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        title = "Wrong Value"
        self.setWindowTitle(title)

        self.main_layout = QVBoxLayout()

        self.message = self.create_message(contents)

        self.message_label = QLabel(self.message)
        self.main_layout.addWidget(self.message_label)

        buttons = QDialogButtonBox.StandardButton.Ok
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)

        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)

    @staticmethod
    def create_message(contents):
        message = ""
        for content in contents:
            message = message + content + "\n"

        return message


