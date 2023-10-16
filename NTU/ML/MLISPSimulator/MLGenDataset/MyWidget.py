from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from myPackage.ParentWidget import ParentWidget
from NTU.ML.ParamGenerater import ParamGenerater
from NTU.ML.CMDRunner import CMDRunner
from .UI import Ui_Form
from NTU.ML.MLISPSimulator.SimulatorConfig import SimulatorConfig
from NTU.ML.MLISPSimulator.SimulatorProjectManager import SimulatorProjectManager

import os
import numpy as np
from tqdm import tqdm
import threading
import ctypes, inspect

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLISPSimulator/MLGenDataset") 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        cmd = CMDRunner()
        self.config = SimulatorConfig().config["c7_config"]
        self.projectMgr = SimulatorProjectManager(self.setting, self.config, cmd)
        self.origin_dir = os.getcwd()
        
        self.setupSettingUI()        
        
    def setupSettingUI(self):
        self.ui.progressBar.hide()
        if self.get_path("project_path") != "./": 
            self.ui.project_path.setText(self.setting["project_path"])
            
        if self.get_path("saved_dir") != "./": self.ui.saved_dir.setText(self.setting["saved_dir"])
        
        
    def controller(self):
        self.ui.load_project_btn.clicked.connect(lambda: self.load_project())
        self.ui.set_saved_dir_btn.clicked.connect(lambda: self.set_saved_dir())
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
        path = QFileDialog.getExistingDirectory(self,"選擇儲存資料夾", self.get_path("saved_folder"))
        if path == "": return
        self.ui.saved_dir.setText(path)
        
        self.set_path('saved_dir', path)
        
    def check_setting(self):
        if self.get_path("project_path") == "./":
            QMessageBox.about(self, "Notice", "project路徑未填")
            return False
        
        if self.get_path("saved_dir") == "./":
            QMessageBox.about(self, "Notice", "儲存路徑未填")
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
        self.ui.progressBar.setMaximum(self.config["gen_num"])
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        
        param_generater = ParamGenerater(bounds=bounds, gen_num=self.config["gen_num"])
        param_norm = param_generater.gen_param()
        param_norm[0] = [0]*len(bounds)
        param_norm[1] = [1]*len(bounds)
        param_denorm = param_generater.denorm_param(param_norm, units=units)
        param_norm = param_generater.norm_param(param_denorm)
        
        param_generater.save_to_csv(self.get_path("saved_dir")+'/param_norm.csv', param_norm)
        param_generater.save_to_csv(self.get_path("saved_dir")+'/param_denorm.csv', param_denorm)
        
        self.projectMgr.set_isp_enable(0)
        self.projectMgr.set_param_value([0]*len(bounds))
        self.projectMgr.build_and_push()
        os.replace(self.setting["project_path"] + "/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg", self.setting["saved_dir"] + f"/unprocessed.jpg")
        
        self.projectMgr.set_isp_enable(1)
        for  i, param in enumerate(tqdm(param_denorm)):
            self.ui.progressBar.setValue(i+1)
            param = [float(x) for x in param]
            self.projectMgr.set_param_value(param)
            self.projectMgr.build_and_push()
            os.replace(self.setting["project_path"] + "/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg", self.setting["saved_dir"] + f"/{i}.jpg")
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
        self.ui.progressBar.hide()
        stop_thread(self.capture_task)
        os.chdir(self.origin_dir)
        
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