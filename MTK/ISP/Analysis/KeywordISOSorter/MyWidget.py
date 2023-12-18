from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from time import sleep
import os
# from .Filter import main as filter_main
from .KeywordISOSorterV3 import main as key_main
from myPackage.ParentWidget import ParentWidget
import subprocess
import ctypes
import sys


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
    image_directory = None
    keyword = None

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            key_main(self.image_directory, self.keyword)
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
        self.ui.btn_browse.clicked.connect(self.browse)
        self.ui.btn_implement.clicked.connect(self.implement)
        self.ui.btn_openFolder.clicked.connect(self.openFolder)
        # self.solver_thread.failed_signal.connect(self.failed)
        # self.solver_thread.finish_signal.connect(self.solver_finish)

    def test(self):
        terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()

        # Bring the terminal window to the front
        ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
        ctypes.windll.user32.SetForegroundWindow(terminal_handle)

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

        self.ui.lineEdit_photoFolderPath.setText(your_path)
        # self.set_btn_enable(self.ui.btn_Compute, True)
        # self.set_btn_enable(self.ui.btn_OpenFolder, True)
        return your_path

    # show Fial/Pass img
    def implement(self):
        if(self.ui.lineEdit_photoFolderPath.text() == ''):
            # show the error message
            QMessageBox.about(self,  "ERROR", "Choose Photo Folder first.")
        else:
            if(self.ui.lineEdit_keyword.text() == ''):
                # show the error message
                QMessageBox.about(self,  "ERROR", "Set a keyword.")
            
            else:
                # 创建确认对话框
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle('')
                msg_box.setText('Replace original file, confirm？')

                # 设置按钮顺序，将Yes按钮放在左边
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.button(QMessageBox.Yes).setText('Yes')
                msg_box.button(QMessageBox.No).setText('No')

                # 显示对话框并处理用户的选择
                reply = msg_box.exec_()
                # 处理用户的选择
                if reply == QMessageBox.Yes:
                    # print('执行操作！')
                    if (self.ui.lineEdit_photoFolderPath.text != ''):
                        # Show terminal in the top
                        terminal_handle = ctypes.windll.kernel32.GetConsoleWindow()
                        ctypes.windll.user32.ShowWindow(terminal_handle, 9)  # SW_RESTORE
                        ctypes.windll.user32.SetForegroundWindow(terminal_handle)

                        # Send path to thread for other .py execution
                        self.solver_thread.image_directory = self.ui.lineEdit_photoFolderPath.text()
                        self.solver_thread.keyword = self.ui.lineEdit_keyword.text()
                        self.solver_thread.start()
                    else:
                        # show the error message
                        QMessageBox.about(
                            self,  "ERROR", "Choose Photo Folder first.")
                else:
                    print('取消操作')


    def openFolder(self):
        if (self.ui.lineEdit_photoFolderPath.text != ''):
            # open folder
            your_path = self.ui.lineEdit_photoFolderPath.text()

            # 防呆

            # For Windows
            os.startfile(your_path)

            # For Linux
            # opener = "open" if sys.platform == "darwin" else "xdg-open"
            # subprocess.call([opener, your_path])
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
        # self.set_all_enable(True)
        QMessageBox.about(self, "Failed", text)

    def solver_finish(self):
        # self.set_all_enable(True)
        # self.statusBar.hide()
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())
