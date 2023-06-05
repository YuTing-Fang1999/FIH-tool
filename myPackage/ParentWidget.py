from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QScrollArea, QFileDialog, QHBoxLayout, QSpacerItem, QSizePolicy
)

import os
import json

class ParentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setting = None
        
    def read_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
        
    def read_setting(self):
        if os.path.exists('setting.json'):
            setting = self.read_json('setting.json')
            return setting
            
        else:
            print("找不到設定檔，重新生成一個新的設定檔")
            return {}
            
    def write_setting(self, setting):
        print('write_setting')
        with open("setting.json", "w") as outfile:
            outfile.write(json.dumps(setting, indent=4))
            
    def get_filefolder(self, key):
        if self.setting == None:
            self.setting = self.read_setting()
        if key not in self.setting:
            self.setting[key] = "./"
        if os.path.exists(self.setting[key]):
            return self.setting[key]
        return "./"
    
    def set_filefolder(self, key, filefolder):
        if self.setting == None:
            self.setting = self.read_setting()
        if key in self.setting and self.setting[key] != filefolder:
            self.setting[key] = filefolder
            self.write_setting(self.setting)
        
    # def closeEvent(self, e):
    #     print("closeEvent")
    #     if self.setting != None and "filefolder" in self.setting and self.setting["filefolder"] != "./":
    #         print('write ', self.setting["filefolder"], ' to filefolder setting')
    #         self.write_setting(self.setting)
        
        
        