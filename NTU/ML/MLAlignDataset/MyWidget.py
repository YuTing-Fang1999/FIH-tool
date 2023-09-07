from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from NTU.ML.MLAlignDataset.UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from NTU.ML.ProjectManager import C7ProjectManager
from NTU.ML.ParamGenerater import ParamGenerater
from NTU.ML.CMDRunner import CMDRunner
from NTU.ML.Camara import Camera
from NTU.ML.Config import Config
import numpy as np
from tqdm import tqdm
from time import sleep
import threading
import ctypes, inspect
import os

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLAlignDataset/") 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        self.set_all_enable(False)
        self.set_btn_enable(self.ui.load_dir_btn, True)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        
    def controller(self):
        self.ui.load_dir_btn.clicked.connect(lambda: self.load_dir())
        self.ui.load_img_btn.clicked.connect(lambda: self.load_img())
        self.ui.start_align_btn.clicked.connect(lambda: self.run())
        
    def load_dir(self):
        path = QFileDialog.getExistingDirectory(self,"選擇project", self.get_path("dir_folder")) # start path
        if path == "": return
        
        self.set_path("dir_folder", path)
        self.ui.dir_label.setText(path)
        
        self.set_btn_enable(self.ui.load_img_btn, True)
        
        if "0.jpg" in os.listdir(path):
            self.ui.img_label.setText(path+"/0.jpg")
            self.set_btn_enable(self.ui.start_align_btn, True)
        
    def load_img(self):
        path, filetype  = QFileDialog.getOpenFileName(self,"選擇ParameterParser.exe", self.get_path("dir_folder")) # start path
        if path == "": return
        self.ui.img_label.setText(path)
        self.set_btn_enable(self.ui.start_align_btn, True)
    
    def run(self):
        if self.ui.start_align_btn.text() == '開始對齊':
            self.start()
        else:
            self.finish()
        
    def start_align(self):
        self.set_all_enable(False)
        self.set_btn_enable(self.ui.start_align_btn, True)
        sleep(3)
        self.finish()
        
    def start(self):
        self.ui.start_align_btn.setText('停止對齊')
        
        # 建立一個子執行緒
        self.align_task = threading.Thread(target=lambda: self.start_align())
        # 當主程序退出，該執行緒也會跟著結束
        self.align_task.daemon = True
        # 執行該子執行緒
        self.align_task.start()

    def finish(self):
        self.set_all_enable(True)
        self.ui.start_align_btn.setText('開始對齊')
        stop_thread(self.align_task)
        
    def set_all_enable(self, enable):
        self.set_btn_enable(self.ui.load_dir_btn, enable)
        self.set_btn_enable(self.ui.load_img_btn, enable)
        self.set_btn_enable(self.ui.start_align_btn, enable)
        
def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            return
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    """
    @profile:強制停掉線程函數
    :param thread:
    :return:
    """
    if thread == None:
        print('thread id is None, return....')
        return
    _async_raise(thread.ident, SystemExit)
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())