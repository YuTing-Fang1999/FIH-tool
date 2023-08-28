from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()


    def controller(self):
        pass
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())