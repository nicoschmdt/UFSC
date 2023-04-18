from PyQt6.QtWidgets import QDialogButtonBox, QDialog, QVBoxLayout, QLabel


class NotAPolygonDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Warning")

        QBtn = QDialogButtonBox.StandardButton.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel("Not a polygon!")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
