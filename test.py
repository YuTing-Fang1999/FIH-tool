#!/usr/bin/python3
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from time import sleep

class IterationThread(QThread):
    update_msg_signal = pyqtSignal(str)
    show_window_signal = pyqtSignal()
    
    def __init__(self, mutex, cond):
        super().__init__()
        self.mtx = mutex
        self.cond = cond

    def run(self):
        for i in range(10):
            self.update_msg_signal.emit('Iteration {}'.format(i))
            sleep(0.5)
            if i == 2 or i == 5:
                self.update_msg_signal.emit('stop thread')
                self.show_window_signal.emit()
                # 當某個執行緒執行到這行程式碼時，它會嘗試獲取 self.mtx 這個鎖。如果鎖已經被其他執行緒佔用，那麼這個執行緒將會等待，直到鎖被釋放為止
                self.mtx.lock()
                try:
                    # 執行緒在這一行會等待，直到其他執行緒通知它可以繼續執行。當其他執行緒通知條件變數時，這個執行緒會被喚醒，然後它將重新嘗試獲取 self.mtx 這個鎖
                    self.cond.wait(self.mtx)
                finally:
                    # 最後，執行緒完成操作後，釋放了鎖 self.mtx，以允許其他執行緒進入這個臨界區域
                    self.mtx.unlock()

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        resLabel = QLabel("Result:")
        self.resFiled = QLineEdit()
        self.buttonStart = QPushButton("Start")

        verticalLayout = QVBoxLayout(self)
        verticalLayout.addWidget(resLabel)
        verticalLayout.addWidget(self.resFiled)
        verticalLayout.addWidget(self.buttonStart)

        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.worker = IterationThread(self.mutex, self.cond)
        self.worker.update_msg_signal.connect(self.update_msg)
        self.worker.show_window_signal.connect(self.show_window)
        self.buttonStart.clicked.connect(self.worker.start)

    def update_msg(self, result):
        self.resFiled.setText(result)
        
    def show_window(self):
        QMessageBox.about(self, "info", "Close this dialog to continue the thread")
        self.cond.wakeOne()

def main():
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()