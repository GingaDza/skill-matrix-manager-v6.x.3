from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SystemInfoTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("システム情報"))
