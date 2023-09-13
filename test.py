import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super(CustomButton, self).__init__(parent)
        self.text1 = "Text1"
        self.text2 = "Text2"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the font and size for the first text
        font1 = QFont("Arial", 12)  # Adjust the font and size as needed
        painter.setFont(font1)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text1)

        # Set the font and size for the second text
        font2 = QFont("Arial", 8)  # Adjust the font and size as needed
        painter.setFont(font2)
        rect = self.rect()
        rect.adjust(0, 20, 0, 0)  # Adjust the position of the second text
        painter.drawText(rect, Qt.AlignCenter, self.text2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    button = CustomButton()
    layout.addWidget(button)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
