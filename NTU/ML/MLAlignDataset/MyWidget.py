from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from NTU.ML.MLAlignDataset.UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from PyQt5.QtCore import pyqtSignal
import numpy as np
import threading
import ctypes, inspect
import os
import cv2
from NTU.ML.MLAlignDataset.aux2 import FeatureExtraction, align

class MyWidget(ParentWidget):
    update_progress_bar_signal = pyqtSignal(int)
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
        self.update_progress_bar_signal.connect(self.ui.progressBar.setValue)
        
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

        jpg_path_list = [f for f in os.listdir(self.ui.dir_label.text()) if ".jpg" in f or ".png" in f]
        self.ui.progressBar.show()
        self.ui.progressBar.setMaximum(len(jpg_path_list))
        # align by this
        img1 = cv2.imdecode( np.fromfile( file = self.ui.img_label.text(), dtype = np.uint8 ), cv2.IMREAD_COLOR )
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
        features1 = FeatureExtraction(img1)

        for i, f in enumerate(jpg_path_list):
            self.update_progress_bar_signal.emit(i+1)
            img0 = cv2.imdecode( np.fromfile( file = os.path.join(self.ui.dir_label.text(),f), dtype = np.uint8 ), cv2.IMREAD_COLOR )
            warped = align(img0, img1, features1)
            cv2.imencode('.jpg', cv2.cvtColor(warped, cv2.COLOR_RGBA2BGR))[1].tofile(os.path.join(self.ui.dir_label.text(),f))
            if f=="0.jpg":
                cv2.imencode('.jpg', cv2.cvtColor(warped, cv2.COLOR_RGBA2BGR))[1].tofile(os.path.join(self.ui.dir_label.text(),"noisy.jpg"))

        os.rename(self.ui.dir_label.text(), self.ui.dir_label.text()+"_align")
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