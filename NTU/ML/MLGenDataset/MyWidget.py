from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from NTU.ML.MLGenDataset.UI import Ui_Form
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

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLGenDataset/") 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        cmd = CMDRunner()
        self.camera = Camera("c7project", cmd)
        self.projectMgr = C7ProjectManager(self.setting, cmd)
        self.config = Config().c7_config
        
        self.setupSettingUI()
        
    # def set_layout_hidden(self):
        
        
        
    def setupSettingUI(self):
        if self.get_path("project_path") != "./": 
            self.ui.project_path.setText(self.setting["project_path"])
            self.set_trigger()
            if "trigger_idx" in self.setting and self.setting["trigger_idx"] != -1:
                self.ui.trigger_comboBox.setCurrentIndex(int(self.setting["trigger_idx"]))
        # else:
            
            
        if self.get_path("exe_path") != "./": self.ui.exe_path.setText(self.setting["exe_path"])
        
        if self.get_path("saved_dir") != "./": self.ui.saved_dir.setText(self.setting["saved_dir"])
        
    def controller(self):
        self.ui.load_project_btn.clicked.connect(lambda: self.load_project())
        self.ui.load_exe_btn.clicked.connect(lambda: self.load_exe())
        self.ui.set_saved_dir_btn.clicked.connect(lambda: self.set_saved_dir())
        self.ui.start_capture_btn.clicked.connect(lambda: self.run())
        
    def load_project(self):
        path = QFileDialog.getExistingDirectory(self,"選擇project", self.get_path("project_folder")) # start path
        if path == "": return
        
        self.setting["project_path"] = path
        
        if not self.projectMgr.is_project():
            self.ui.project_path.setText("Load project fail, 請確認是否為c7project")
            return
        
        self.ui.project_path.setText(path)
        self.setting["project_folder"] = '/'.join(path.split('/')[:-1])
        self.setting["project_name"] = path.split('/')[-1]
        self.write_setting(self.setting_folder + "setting.json")
        self.set_trigger()
        
    def set_trigger(self):
        trigger_data=self.projectMgr.get_trigger_data()
        item_names = ["Gain {:>2}x (gain start {} end {})".format(int(d[2]), d[2], d[3]) for d in trigger_data]
        self.ui.trigger_comboBox.clear()
        self.ui.trigger_comboBox.addItems(item_names) # -> set_trigger_idx 0
        
    def load_exe(self):
        path, filetype  = QFileDialog.getOpenFileName(self,"選擇ParameterParser.exe", self.get_path("project_folder")) # start path
        if path == "": return
        self.ui.exe_path.setText(path)
        
        self.set_path('project_folder', '/'.join(path.split('/')[:-1]))
        self.set_path('exe_path', path)
        
    def set_saved_dir(self):
        path = QFileDialog.getExistingDirectory(self,"選擇儲存資料夾", self.get_path("saved_folder"))
        if path == "": return
        self.ui.saved_dir.setText(path)
        
        self.set_path('saved_dir', path)
        
    def check_setting(self):
        if self.get_path("project_path") == "./":
            QMessageBox.about(self, "Notice", "project路徑未填")
            return False
        
        if self.get_path("exe_path") == "./":
            QMessageBox.about(self, "Notice", "exe路徑未填")
            return False
        
        if self.get_path("saved_dir") == "./":
            QMessageBox.about(self, "Notice", "儲存路徑未填")
            return False
        
        if self.ui.bin_name_edit.text() == "":
            QMessageBox.about(self, "Notice", "bin檔名未填")
            return False
        
        self.setting["bin_name"] = self.ui.bin_name_edit.text()
        self.setting["trigger_idx"] = self.ui.trigger_comboBox.currentIndex()
        self.write_setting(self.setting_folder + "setting.json")
        
        return True
    
    def run(self):
        if self.ui.start_capture_btn.text() == '開始拍攝':
            self.start()
        else:
            self.finish()
        
    def start_capture(self):
        bounds = None
        for key in self.config:
            if bounds is None:
                bounds = np.array(self.config[key]["bounds"])
            else:
                bounds = np.concatenate((bounds, np.array(self.config[key]["bounds"])))
        print('範圍設定\n', bounds)
        # self.finish()
        # return
    
        param_generater = ParamGenerater(bounds=bounds, gen_num=Config().gen_num)
        param_norm = param_generater.gen_param()
        param_norm[0] = [0]*len(bounds)
        param_norm[1] = [1]*len(bounds)
        param_denorm = param_generater.denorm_param(param_norm, step=Config().step)
        param_norm = param_generater.norm_param(param_denorm)
        
        param_generater.save_to_csv(self.get_path("saved_dir")+'/param_norm.csv', param_norm)
        param_generater.save_to_csv(self.get_path("saved_dir")+'/param_denorm.csv', param_denorm)
        
        for  i, param in enumerate(tqdm(param_denorm)):
            param = [float(x) for x in param]
            if i % 10 == 0:
                self.camera.clear_camera_folder()
                sleep(2)
            self.projectMgr.set_param_value(param)
            self.projectMgr.build_and_push()
            sleep(7)
            self.camera.capture(path="{}/{}".format(self.get_path("saved_dir"),i), focus_time = 5, save_time = 0.5, transfer_time = 0.5, capture_num = 1)
        
        self.finish()
        
    def start(self):
        if self.check_setting() == False: return
        self.ui.start_capture_btn.setText('停止拍攝')
        
        # 建立一個子執行緒
        self.capture_task = threading.Thread(target=lambda: self.start_capture())
        # 當主程序退出，該執行緒也會跟著結束
        self.capture_task.daemon = True
        # 執行該子執行緒
        self.capture_task.start()

    def finish(self):
        self.ui.start_capture_btn.setText('開始拍攝')
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