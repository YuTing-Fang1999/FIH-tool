from PyQt5.QtWidgets import QWidget

import os
import json

class ParentWidget(QWidget):
    def __init__(self, setting_folder="./"):
        super().__init__()
        self.setting_folder = setting_folder
        self.setting = self.read_setting(setting_folder + 'setting.json')
        
    def read_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
        
    def read_setting(self, setting_path):
        if os.path.exists(setting_path):
            setting = self.read_json(setting_path)
            return setting
            
        else:
            print("找不到設定檔，重新生成一個新的設定檔")
            return {}
            
    def write_setting(self, setting_path):
        print('write_setting')
        with open(setting_path, "w") as outfile:
            outfile.write(json.dumps(self.setting, indent=4))
            
    def get_path(self, key):
        if self.setting == None:
            self.setting = self.read_setting()
        if key not in self.setting:
            self.setting[key] = "./"
        if os.path.exists(self.setting[key]):
            return self.setting[key]
        return "./"
    
    def set_path(self, key, path):
        if self.setting == None:
            self.setting = self.read_setting()
        if key not in self.setting or (key in self.setting and self.setting[key] != path):
            self.setting[key] = path
            self.write_setting(self.setting_folder + "setting.json")
        
    # def closeEvent(self, e):
    #     print("closeEvent")
    #     if self.setting != None and "filefolder" in self.setting and self.setting["filefolder"] != "./":
    #         print('write ', self.setting["filefolder"], ' to filefolder setting')
    #         self.write_setting(self.setting)
        
        
        