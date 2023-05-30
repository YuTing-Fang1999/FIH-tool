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
        
    def read_setting(self):
        if os.path.exists('setting.json'):
            with open('setting.json', 'r') as f:
                setting = json.load(f)
                if not os.path.exists(setting["filefolder"]):
                    setting["filefolder"] = "./"
                return setting
            
        else:
            print("找不到設定檔，重新生成一個新的設定檔")
            return {
                "filefolder": "./"
            }
            
    def write_setting(self, setting):
        print('write_setting')
        with open("setting.json", "w") as outfile:
            outfile.write(json.dumps(setting, indent=4))
            
    def get_filefolder(self):
        if self.setting == None:
            self.setting = self.read_setting()
        if os.path.exists(self.setting["filefolder"]):
            return self.setting["filefolder"]
        return "./"
    
    def set_filefolder(self, filefolder):
        if self.setting == None:
            self.setting = self.read_setting()
        if "filefolder" in self.setting and self.setting["filefolder"] != filefolder:
            self.setting["filefolder"] = filefolder
            self.write_setting(self.setting)
        
    # def closeEvent(self, e):
    #     print("closeEvent")
    #     if self.setting != None and "filefolder" in self.setting and self.setting["filefolder"] != "./":
    #         print('write ', self.setting["filefolder"], ' to filefolder setting')
    #         self.write_setting(self.setting)
        
        
        