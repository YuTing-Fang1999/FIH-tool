from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.is_open = False  # 下拉式选单的状态，默认为关闭

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.toggle_button = QPushButton("Toggle")
        self.toggle_button.clicked.connect(self.toggle_dropdown)
        layout.addWidget(self.toggle_button)

        self.dropdown_widget = QWidget()
        dropdown_layout = QVBoxLayout()
        self.dropdown_widget.setLayout(dropdown_layout)

        self.label1 = QLabel("Item 1")
        self.label2 = QLabel("Item 2")
        dropdown_layout.addWidget(self.label1)
        dropdown_layout.addWidget(self.label2)

    def toggle_dropdown(self):
        if self.is_open:
            self.close_dropdown()
        else:
            self.open_dropdown()

    def open_dropdown(self):
        self.layout().addWidget(self.dropdown_widget)
        self.is_open = True

    def close_dropdown(self):
        self.layout().removeWidget(self.dropdown_widget)
        self.is_open = False

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
