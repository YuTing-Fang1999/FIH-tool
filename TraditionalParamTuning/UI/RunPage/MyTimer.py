from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel
)

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

class MyTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.setup_UI()

    def setup_UI(self):
        HLayout = QHBoxLayout(self)
        self.label_time = QLabel("Time")
        self.label_time.setAlignment(Qt.AlignCenter)
        # self.label_time.setStyleSheet("font-family:Agency FB; font-size:30pt; width: 100%; height: 100%;")
        HLayout.addWidget(self.label_time)

        self.mytimer = QTimer(self)
        self.mytimer.timeout.connect(self.onTimer)

    def onTimer(self):
        self.counter += 1
        total_sec = self.counter
        hour = max(0, total_sec//3600)
        minute = max(0, total_sec//60 - hour * 60)
        sec = max(0, (total_sec - (hour * 3600) - (minute * 60)))
        # show time_counter (by format)
        self.label_time.setText(str(f"{hour}:{minute:0>2}:{sec:0>2}"))

    def startTimer(self):
        self.counter = -1
        self.onTimer()
        self.mytimer.start(1000)

    def stopTimer(self):
        self.mytimer.stop()

    def continueTimer(self):
        self.mytimer.start(1000)
