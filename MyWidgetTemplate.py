from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
# from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import numpy as np

class SolverThread(QThread):
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.finish_signal.emit()
        except Exception as error:
            print(error)
            self.failed_signal.emit("Failed...\n"+str(error))            
            

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        # self.ui = Ui_Form()
        # self.ui.setupUi(self)
        self.solver_thread = SolverThread()
        self.controller()

    def controller(self):
        self.solver_thread.failed_signal.connect(self.failed)
        self.solver_thread.finish_signal.connect(self.solver_finish)

    def failed(self, text="Failed"):
        QMessageBox.about(self, "Failed", text)    

    def solver_finish(self):
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())