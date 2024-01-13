from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from NTU.ML.ParamGenerater import ParamGenerater
from NTU.ML.CMDRunner import CMDRunner
from NTU.ML.MLISPSimulator.SimulatorConfig import SimulatorConfig
from NTU.ML.MLISPSimulator.SimulatorProjectManager import SimulatorProjectManager
import numpy as np
from tqdm import tqdm
from time import sleep
import threading
import ctypes, inspect
import os

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLISPSimulator/MLPushParam/") 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        cmd = CMDRunner()
        self.config = SimulatorConfig().config["c7_config"]
        self.projectMgr = SimulatorProjectManager(self.setting, self.config, cmd)
        self.param_norm = None
        
        self.setupSettingUI()
        
    def setupSettingUI(self):
        if self.get_path("project_path") != "./": 
            self.ui.project_path.setText(self.setting["project_path"])
        
        if self.get_path("saved_dir") != "./": 
            self.ui.saved_dir.setText(self.setting["saved_dir"])
        
    def controller(self):
        self.ui.load_project_btn.clicked.connect(lambda: self.load_project())
        self.ui.set_saved_dir_btn.clicked.connect(lambda: self.set_saved_dir())
        self.ui.load_txt_btn.clicked.connect(lambda: self.load_txt())
        self.ui.start_btn.clicked.connect(lambda: self.run())
        
    def load_project(self):
        path = QFileDialog.getExistingDirectory(self,"選擇project", self.get_path("project_folder")) # start path
        if path == "": return
        
        self.setting["project_path"] = path
        
        if not self.projectMgr.is_project():
            self.ui.project_path.setText("Load project fail, 請確認是否為c7project")
            return
        
        self.ui.project_path.setText(path)
        self.set_path("project_folder", '/'.join(path.split('/')[:-1]))
        self.set_path("project_name", path.split('/')[-1])
        
    def set_saved_dir(self):
        path = QFileDialog.getExistingDirectory(self,"選擇儲存資料夾", self.get_path("saved_dir"))
        if path == "": return
        self.ui.saved_dir.setText(path)
        
        self.set_path('saved_dir', path)
        
    def load_txt(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                            "Open file",
                                                            self.get_path("param_txt_folder"),  # start path
                                                            '*.txt')

        if filepath == '':
            return
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_path("param_txt_folder", filefolder)
        self.ui.txt_path_label.setText(filepath)
        self.img_name = filepath.split('/')[-1].split('.')[0] +".jpg"
        self.ui.img_path_label.setText(self.img_name)
        
        with open(filepath) as f:
            text = f.read().replace('[', '').replace(']', '').replace(',', ' ')
            text = text.split()
            # print(text)
            param_norm = [float(t) for t in text if t != '']
            
        self.ui.param_label.setText("{}".format(param_norm))
        self.param_norm = param_norm
        # print(param_norm)
        
    def check_setting(self):
        if self.get_path("project_path") == "./":
            QMessageBox.about(self, "Notice", "project路徑未填")
            return False
        
        if self.get_path("saved_dir") == "./":
            QMessageBox.about(self, "Notice", "儲存路徑未填")
            return False
        
        if self.ui.txt_path_label.text() == "":
            QMessageBox.about(self, "Notice", "param.txt 還沒load")
            return False
        
        return True
    
    def run(self):
        if self.ui.start_btn.text() == 'Start':
            self.start()
        else:
            self.finish()
        
    def start_gen(self):
        bounds = None
        units = None
        for ISP_key in self.config["ISP"]:
            ISP_block = self.config["ISP"][ISP_key]
            for tag_key in ISP_block["tag"]:
                if "bounds" not in ISP_block["tag"][tag_key]: continue
                if bounds is None:
                    bounds = np.array(ISP_block["tag"][tag_key]["bounds"])
                    units = np.array(ISP_block["tag"][tag_key]["units"])
                else:
                    bounds = np.concatenate((bounds, np.array(ISP_block["tag"][tag_key]["bounds"])))
                    units = np.concatenate((units, np.array(ISP_block["tag"][tag_key]["units"])))
                    
        print('範圍設定\n', bounds)
        print('單位設定\n', units)
        # self.finish()
        # return
        param_generater = ParamGenerater(bounds=bounds, gen_num=0)
        param_norm = self.param_norm
        assert len(param_norm) == len(bounds)
        param_denorm = param_generater.denorm_param(param_norm, units=units)
        self.projectMgr.set_isp_enable(1)
        self.projectMgr.set_param_value(param_denorm)
        self.projectMgr.build_and_push()
        # os.replace(self.setting["project_path"] + "/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg", self.setting["saved_dir"] + f"/{self.img_name}")
        os.replace(self.setting["project_path"] + "/iso1600/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg", self.setting["saved_dir"] + f"/{self.img_name}")
        self.finish()
        
    def start(self):
        if self.check_setting() == False: return
        self.ui.start_btn.setText('Stop')
        
        # 建立一個子執行緒
        self.capture_task = threading.Thread(target=lambda: self.start_gen())
        # 當主程序退出，該執行緒也會跟著結束
        self.capture_task.daemon = True
        # 執行該子執行緒
        self.capture_task.start()

    def finish(self):
        self.ui.start_btn.setText('Start')
        stop_thread(self.capture_task)
        
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