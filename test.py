import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap

class HoverButton(QToolButton):
    def __init__(self, text, image_path, parent=None):
        super(HoverButton, self).__init__(parent)
        self.setText(text)
        self.image_path = image_path
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIconSize(QSize(50, 50))
        self.setAutoRaise(True)
        self.setStyleSheet("QToolButton { border: none; }")
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self and event.type() == QEvent.Enter:
            pixmap = QPixmap(self.image_path)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            popup = QWidget(self)
            layout = QVBoxLayout(popup)
            layout.addWidget(label)
            popup.setLayout(layout)
            popup.move(self.mapToGlobal(self.rect().bottomRight()))
            popup.show()
            popup.setStyleSheet("background-color: white; border: 1px solid black;")
            self.popup = popup

        if obj == self and event.type() == QEvent.Leave:
            if hasattr(self, 'popup'):
                self.popup.close()

        return super(HoverButton, self).eventFilter(obj, event)

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout()

    button = HoverButton("Hover Button", "image.png")
    layout.addWidget(button)
    
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
