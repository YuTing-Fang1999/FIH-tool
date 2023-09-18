from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # self.setupUi()
        self.controller()

    def setupUi(self):
        for i in range(3):
            for j in range(4):
                label = QLabel()
                label.setText("#")
                style = "border: 1px solid gray; border-radius: 0px;"
                if j==0:
                    style += "border-left: 2px solid white;"
                if j==2:
                    style += "border-right: 2px solid white;"
                if i==0 and j<=2:
                    style += "border-top: 2px solid white;"
                if i==2 and j<=2:
                    style += "border-bottom: 2px solid white;"
                label.setStyleSheet(style)
                self.ui.CCM_grid.addWidget(label, i, j)
    def controller(self):
        pass
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())