import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer

class HoverLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.hover_timer = QTimer(self)
        self.hover_timer.timeout.connect(self.on_hover_timer_timeout)
        self.hover_timer.setInterval(1000)  # 1000 milliseconds = 1 second
        self.is_hovered = False

    def enterEvent(self, event):
        if not self.is_hovered:
            self.is_hovered = True
            self.hover_timer.start()

    def leaveEvent(self, event):
        self.is_hovered = False
        self.hover_timer.stop()

    def on_hover_timer_timeout(self):
        # This method will be called after 1 second of hovering
        print("Label has been hovered for 1 second")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    label = HoverLabel("Hover over me for 1 second", window)
    label.setGeometry(100, 100, 200, 50)
    window.setGeometry(100, 100, 400, 200)
    window.show()
    sys.exit(app.exec_())
