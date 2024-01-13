from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from myPackage.ParentWidget import ParentWidget
from NTU.ML.ParamGenerater import ParamGenerater
from NTU.ML.CMDRunner import CMDRunner
from .UI import Ui_Form
from NTU.ML.MLISPSimulator.SimulatorConfig import SimulatorConfig
from NTU.ML.MLISPSimulator.SimulatorProjectManager import SimulatorProjectManager
from scipy.stats import qmc
from scipy.stats import uniform
import numpy as np
import time
import shutil

import os
import numpy as np
from tqdm import tqdm
import threading
import ctypes, inspect

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLISPSimulator/MLGenDataset/") 
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
        path = QFileDialog.getExistingDirectory(self,"選擇儲存資料夾", self.get_path("saved_dir") )
        if path == "": return
        self.ui.saved_dir.setText(path)
        
        self.set_path('saved_dir', path)
        
    def check_setting(self):
        if self.get_path("project_path") == "./":
            QMessageBox.about(self, "Notice", "project路徑未填")
            return False
        
        if self.get_path("saved_dir") == "./":
            QMessageBox.about(self, "Notice", "儲存路徑未填或是未存在")
            return False
        
        return True
    
    def run(self):
        if self.ui.start_btn.text() == 'Start':
            self.start()
                
        else:
            self.finish()
        
    def start_gen(self):
        start_time = time.time()
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
        print(len(bounds), len(units))
        # self.finish()
        # return
        self.ui.progressBar.setMaximum(self.config["gen_num"])
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.show()
        
        if len(os.listdir(self.get_path("saved_dir"))) == 0:
            assert self.RELOAD == False
            param_generater = ParamGenerater(bounds=bounds, gen_num=self.config["gen_num"])
            param_norm = param_generater.gen_param()
            param_norm[0] = [0]*len(bounds)
            param_norm[1] = [1]*len(bounds)
            param_denorm = param_generater.denorm_param(param_norm, units=units)
            param_norm = param_generater.norm_param(param_denorm)
            
            print('save_to_csv')
            param_generater.save_to_csv(self.get_path("saved_dir")+'/param_norm.csv', param_norm)
            param_generater.save_to_csv(self.get_path("saved_dir")+'/param_denorm.csv', param_denorm)
        else:
            assert self.RELOAD == True
            print('detect param is exist, load param')
            with open(self.get_path("saved_dir")+'/param_norm.csv', 'r') as f:
                param_norm = np.loadtxt(f, delimiter=',')
            with open(self.get_path("saved_dir")+'/param_denorm.csv', 'r') as f:
                param_denorm = np.loadtxt(f, delimiter=',')
            
            print(param_norm[0])
            print(param_denorm[0])
        
        if os.path.exists(self.setting["project_path"] + "/iso1600/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg"):
            os.remove(self.setting["project_path"] + "/iso1600/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg")
            
        self.projectMgr.set_isp_enable(1)
        for  i, param in enumerate(tqdm(param_denorm)):
            if os.path.exists(self.setting["saved_dir"] + f"/{i}.jpg"):
                continue
            
            self.ui.progressBar.setValue(i)
            param = [float(x) for x in param]
            self.projectMgr.set_param_value(param)
            self.projectMgr.build_and_push()
            os.replace(self.setting["project_path"] + "/iso1600/Output/Out_0_0_POSTFILT_ipeout_pps_display_FULL.jpg", self.setting["saved_dir"] + f"/{i}.jpg")

        shutil.copyfile(self.setting["saved_dir"] + f"/0.jpg", self.setting["saved_dir"] + f"/unprocessed.jpg")
        end_time = time.time()
        print(f'total time: {end_time-start_time}')
        self.finish()
        
    def start(self):
        if self.check_setting() == False: return
        self.RELOAD = False
        if len(os.listdir(self.get_path("saved_dir"))) != 0:
            QMessageBox.about(self, "Notice", "偵測到已有資料，將會接續上次的資料繼續產生")
            self.RELOAD = True
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