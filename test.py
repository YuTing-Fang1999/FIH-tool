# import numpy as np
# arr = np.array([0.0927, 0.5928, 0.0964, 0.8743, 0.168, 0.0212, 0.9929])
# arr[3:] /= 2
# print(arr.tolist())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal

class TextEditWithChangeEvent(QTextEdit):
    change_event = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        # Call the base class implementation
        super().keyPressEvent(event)
        # Emit the change_event signal whenever a key is pressed
        self.change_event.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = TextEditWithChangeEvent(self)
        self.text_edit.change_event.connect(self.handle_change_event)

        self.setCentralWidget(self.text_edit)

    def handle_change_event(self):
        # Handle the change event here
        print("Text changed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
