from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from UI import Ui_Form  # .
from time import sleep
import os
from Filter import main as filter_main  # .
from ParentWidget import ParentWidget
import subprocess


class WorkerThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        sleep(5)
        print("i")


class SolverThread(QThread):
    update_status_bar_signal = pyqtSignal(str)
    failed_signal = pyqtSignal(str)
    finish_signal = pyqtSignal()
    data = None

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # . . . (要執行的程式)
            filter_main()
            self.finish_signal.emit()
        except Exception as error:
            print(error)
            self.update_status_bar_signal.emit("Failed...")
            self.failed_signal.emit("Failed...\n"+str(error))


class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.solver_thread = SolverThread()
        self.controller()
        self.setupUi()

    def controller(self):
        self.ui.btn_Browse.clicked.connect(self.browse)
        self.ui.btn_Compute.clicked.connect(self.compute)
        self.ui.btn_OpenFolder.clicked.connect(self.openFolder)
        self.solver_thread.failed_signal.connect(self.failed)
        self.solver_thread.finish_signal.connect(self.solver_finish)

    def setupUi(self):
        # self.set_btn_enable(self.ui.btn_Compute, False)
        # self.set_btn_enable(self.ui.btn_OpenFolder, False)
        pass

    def browse(self):
        your_path = QFileDialog.getExistingDirectory(
            self, "選擇Data Path", self.get_path("./"))

        if your_path == '':
            return
        # self.solver_thread.dir_path = filepath
        filefolder = '/'.join(your_path.split('/')[:-1])
        self.set_path("./", filefolder)

        self.ui.lineEdit_FolderPath.setText(your_path)
        # self.set_btn_enable(self.ui.btn_Compute, True)
        # self.set_btn_enable(self.ui.btn_OpenFolder, True)
        return your_path

    # show cmd in front/ show on btn
    def compute(self):
        if (self.ui.lineEdit_FolderPath.text != ''):
            self.solver_thread.start()
            input()
            sys.exit()
        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")

    def openFolder(self):
        if (self.ui.lineEdit_FolderPath.text != ''):
            # open folder
            your_path = self.ui.lineEdit_FolderPath.text()

            # 防呆

            # For Windows
            # os.startfile(your_path)

            # For Linux
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, your_path])
        else:
            # show the error message
            QMessageBox.about(
                self,  "ERROR", "Choose Photo Folder first.")

    def set_btn_enable(self, btn: QPushButton, enable):
        if enable:
            style = "QPushButton {background:rgb(68, 114, 196); color: white;}"
        else:
            style = "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        btn.setStyleSheet(style)
        btn.setEnabled(enable)

    def failed(self, text="Failed"):
        self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)

    def solver_finish(self):
        self.set_all_enable(True)
        self.statusBar.hide()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
