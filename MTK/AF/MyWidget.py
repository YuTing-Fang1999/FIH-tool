from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os
import json
from MTK.AF import main_UIParser
import threading
import time

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        
        #global variable
        self.CONFIG_FOLDER = "MTK\\AF\\config\\"
        self.PHOTO_DIR = ""
        self.LOG_DIR = ""
        self.OUTPUT_DIR = ""
        self.PROJECT_NAME = ""
        self.isConfig = False
        
    def controller(self):
        self.ui.configButton.clicked.connect(self.writeNewConfig)
        self.ui.readImagesDirButton.clicked.connect(self.showPhotoFileDialog)
        self.ui.readLogDirButton.clicked.connect(self.showLogFileDialog)
        self.ui.outputDirButton.clicked.connect(self.showOutputFileDialog)
        self.ui.executeParserButton.clicked.connect(self.executeParser)
        
        self.ui.projectNameEntry.textChanged.connect(self.stateUpdate)
        
        
    def textchanged(self, text):
        print("Changed: " + text)
        
    #function setup
    def detectParserReady(self):
        if self.isConfig and self.PHOTO_DIR != "" and self.LOG_DIR != "" and self.OUTPUT_DIR != "":
            self.ui.executeParserButton.setEnabled(True)
            # executeParserButton["state"] = tk.NORMAL
        else:
            self.ui.executeParserButton.setEnabled(False)
            # executeParserButton["state"] = tk.DISABLED

    def showPhotoFileDialog(self):
        # global PHOTO_DIR
        # PHOTO_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇圖片資料夾")
        # readImagesDirLabel["text"] = PHOTO_DIR
        # detectParserReady()
        
        # Open file dialog
        self.PHOTO_DIR = QFileDialog.getExistingDirectory(self,"選擇圖片資料夾", self.get_path("MTK_AF_folder"))
        if self.PHOTO_DIR == "": return
        self.ui.readImagesDirLabel.setText(self.PHOTO_DIR)
        self.set_path('MTK_AF_folder', '/'.join(self.PHOTO_DIR.split('/')[:-1]))
        self.detectParserReady()
        
        
    def showLogFileDialog(self):
        # global LOG_DIR
        # LOG_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇log資料夾")
        # readLogDirLabel["text"] = LOG_DIR
        # detectParserReady()
        
        # Open file dialog
        self.LOG_DIR = QFileDialog.getExistingDirectory(self,"選擇log資料夾", self.get_path("MTK_AF_folder"))
        if self.LOG_DIR == "": return
        self.ui.readLogDirLabel.setText(self.LOG_DIR)
        self.set_path('MTK_AF_folder', '/'.join(self.LOG_DIR.split('/')[:-1]))
        self.detectParserReady()

    def showOutputFileDialog(self):
        # global OUTPUT_DIR
        # OUTPUT_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇匯出資料夾")
        # outputDirLabel["text"] = OUTPUT_DIR
        # detectParserReady()
        
        # Open file dialog
        self.OUTPUT_DIR = QFileDialog.getExistingDirectory(self,"選擇匯出資料夾", '/'.join(self.get_path("MTK_AF_output_folder").split('/')[:-1]))
        if self.OUTPUT_DIR == "": return
        self.ui.outputDirLabel.setText(self.OUTPUT_DIR)
        self.set_path('MTK_AF_output_folder', self.OUTPUT_DIR)
        self.detectParserReady()


    def writeNewConfig(self):
        # global PROJECT_NAME, isConfig
        #set all label bg color as default
        # projectNameLabel.config(bg = 'SystemButtonFace')
        # filterKeywordLabel.config(bg = 'SystemButtonFace')
        # endKeywordLabel.config(bg = 'SystemButtonFace')
        
        # if projectNameEntry.get() == "":
        #     projectNameLabel.config(bg = "red")
        #     configStatusLabel["text"] = "部分欄位為空，請重新設定"
        if self.ui.projectNameEntry.text() == "":
            self.ui.configStatusLabel.setText("專案名稱為空，請重新設定")
            
        # if filterKeywordText.get(1.0, 'end-1c') == "":
        #     filterKeywordLabel.config(bg = "red")
        #     configStatusLabel["text"] = "部分欄位為空，請重新設定"
        if self.ui.filterKeywordText.text() == "":
            self.ui.configStatusLabel.setText("保留關鍵字為空，請重新設定")
        
        # if endKeywordEntry.get() == "":
        #     endKeywordLabel.config(bg = "red")
        #     configStatusLabel["text"] = "部分欄位為空，請重新設定"
        if self.ui.endKeywordEntry.text() == "":
            self.ui.configStatusLabel.setText("結束關鍵字為空，請重新設定")
        
        # if projectNameEntry.get() != "" and filterKeywordText.get(1.0, 'end-1c') != "" and endKeywordEntry.get() != "":
        if self.ui.projectNameEntry.text() != "" and self.ui.filterKeywordText.text() != "" and self.ui.endKeywordEntry.text() != "":
            # PROJECT_NAME = projectNameEntry.get()
            self.PROJECT_NAME = self.ui.projectNameEntry.text()
            
            writeConfigs = dict()
            
            # writeConfigs["project_name"] = projectNameEntry.get()
            # writeConfigs["previous_second_to_start_log"] = int(prevSecClipSpinbox.get())
            writeConfigs["project_name"] = self.ui.projectNameEntry.text()
            writeConfigs["previous_second_to_start_log"] = int(self.ui.prevSecClipSpinbox.value())
            
            filterKeywordList = []
            for i in range(len(self.ui.filterKeywordText.text().split("\n"))):
                if self.ui.filterKeywordText.text().split("\n")[i] == "":
                    continue
                else:
                    filterKeywordList.append(self.ui.filterKeywordText.text().split("\n")[i])
            writeConfigs["log_keyword"] = filterKeywordList
            
            writeConfigs["save_keyword"] = [self.ui.endKeywordEntry.text()]
            
            with open(self.CONFIG_FOLDER + self.ui.projectNameEntry.text() + ".json", 'w') as outFile:
                json.dump(writeConfigs, outFile, indent = 4)
            # configStatusLabel["text"] = "設定檔寫入完成!"
            self.ui.configStatusLabel.setText("設定檔寫入完成!")
            self.isConfig = True
            self.detectParserReady()

    def stateUpdate(self, text):
        self.PROJECT_NAME = ""
        self.ui.statusLabel.setText("")
        if len(text) == 0:
            self.ui.configButton.setEnabled(False)
            # filterKeywordText.delete(1.0, 'end-1c')
            # endKeywordEntry.delete(0, tk.END)
            self.ui.filterKeywordText.setText("")
            self.ui.endKeywordEntry.setText("")
        else:
            # configButton["state"] = tk.NORMAL
            self.ui.configButton.setEnabled(True)
        
        # configStatusLabel["text"] = "請先填入專案名稱與相關設定"
        self.ui.configStatusLabel.setText("請先填入專案名稱與相關設定")
        config_files = os.listdir(self.CONFIG_FOLDER)
        self.isConfig = False
        self.detectParserReady()

        for config_file in config_files:
            config_file_name = config_file.split(".")[0]        
            if text == config_file_name:
                #有匹配到就使用配置檔的設定，並在更新狀態顯示
                # configStatusLabel["text"] = "已有該專案配置檔"
                self.ui.configStatusLabel.setText("已有該專案配置檔")
                self.PROJECT_NAME = config_file_name
                with open(self.CONFIG_FOLDER + config_file) as jsonFile:
                    config = json.load(jsonFile)
                
                # defaultPrevSec.set(config["previous_second_to_start_log"])
                self.ui.prevSecClipSpinbox.setValue(config["previous_second_to_start_log"])
                
                # filterKeywordText.delete(1.0, 'end-1c')
                self.ui.filterKeywordText.setText("")

                for i in range(len(config["log_keyword"])):
                    if i == len(config["log_keyword"]) - 1:
                        # filterKeywordText.insert(tk.INSERT, str(config["log_keyword"][i]))
                        self.ui.filterKeywordText.setText(self.ui.filterKeywordText.text()+str(config["log_keyword"][i]))
                    else:
                        # filterKeywordText.insert(tk.INSERT, str(config["log_keyword"][i]) + '\n')
                        self.ui.filterKeywordText.setText(self.ui.filterKeywordText.text()+str(config["log_keyword"][i]) + '\n')
                
                # endKeywordEntry.delete(0, tk.END)
                # endKeywordEntry.insert(0, str(config["save_keyword"][0]))
                # isConfig = True
                # detectParserReady()
                self.ui.endKeywordEntry.setText(str(config["save_keyword"][0]))
                self.isConfig = True
                self.detectParserReady()
                break

    def executeProgress(self, parser):
        #block all user-type widget when parsing logs
        # projectNameEntry["state"] = "disable"
        self.ui.projectNameEntry.setEnabled(False)
        # prevSecClipSpinbox["state"] = "disable"
        self.ui.prevSecClipSpinbox.setEnabled(False)
        # filterKeywordText["state"] = "disable"
        self.ui.filterKeywordText.setEnabled(False)
        # filterKeywordText["bg"] = "#F0F0F0"
        # filterKeywordText["fg"] = "#777777"
        # endKeywordEntry["state"] = "disable"
        self.ui.endKeywordEntry.setEnabled(False)
        # configButton["state"] = "disable"
        self.ui.configButton.setEnabled(False)
        # readImagesDirButton["state"] = "disable"
        self.ui.readImagesDirButton.setEnabled(False)
        # readLogDirButton["state"] = "disable"
        self.ui.readLogDirButton.setEnabled(False)
        # outputDirButton["state"] = "disable"
        self.ui.outputDirButton.setEnabled(False)
        # executeParserButton["state"] = "disable"
        self.ui.executeParserButton.setEnabled(False)
        # executeParserButton["text"] = "Log解析中"
        self.ui.executeParserButton.setText("Log解析中")
        # executeParserProgressBar.grid(row = 12, column = 0, pady = 5, columnspan=2)
        
        prev = 0
        # executeParserProgressBar["value"] = prev
        self.ui.executeParserProgressBar.setValue(prev)
        i=0
        while(True):
            #config UI when parse error
            if parser.isParseError:
                # tk.messagebox.showwarning("解析錯誤", parser.parseErrorMessage)
                QMessageBox.about(self, "解析錯誤", parser.parseErrorMessage)
                # projectNameEntry["state"] = "normal"
                self.ui.projectNameEntry.setEnabled(True)
                # prevSecClipSpinbox["state"] = "normal"
                self.ui.prevSecClipSpinbox.setEnabled(True)
                # filterKeywordText["state"] = "normal"
                self.ui.filterKeywordText.setEnabled(True)
                # filterKeywordText["bg"] = "SystemWindow"
                # filterKeywordText["fg"] = "SystemWindowText"
                # endKeywordEntry["state"] = "normal"
                self.ui.endKeywordEntry.setEnabled(True)
                # configButton["state"] = "normal"
                self.ui.configButton.setEnabled(True)
                # readImagesDirButton["state"] = "normal"
                self.ui.readImagesDirButton.setEnabled(True)
                # readLogDirButton["state"] = "normal"
                self.ui.readLogDirButton.setEnabled(True)
                # outputDirButton["state"] = "normal"
                self.ui.outputDirButton.setEnabled(True)
                # executeParserButton["state"] = "normal"
                self.ui.executeParserButton.setEnabled(True)
                # executeParserButton["text"] = "執行"
                self.ui.executeParserButton.setText("執行")
                # executeParserProgressBar.grid_forget()
                self.ui.executeParserProgressBar.hide()
                break
            
            #update progress bar
            time.sleep(0.001) #do not modify. Remove this line will cause stuck, set longer will make warning message not pop up.
            progressAtWork = int(parser.currentProcessPhotoNum / parser.totalPhotoNum * 100)
            if prev != progressAtWork:
                for i in range(prev, progressAtWork+1):
                    time.sleep(0.001) #shorter makes progress update more frequently
                    # executeParserProgressBar["value"] = i
                    self.ui.executeParserProgressBar.setValue(i)
                prev = progressAtWork
            
            #update status when parsing
            # statusLabel["text"] = "".join(parser.parseState)
            self.ui.statusLabel.setText("".join(parser.parseState))
            
            #log parse complete
            if parser.currentProcessPhotoNum == parser.totalPhotoNum:
                # projectNameEntry["state"] = "normal"
                self.ui.projectNameEntry.setEnabled(True)
                # prevSecClipSpinbox["state"] = "normal"
                self.ui.prevSecClipSpinbox.setEnabled(True)
                # filterKeywordText["state"] = "normal"
                self.ui.filterKeywordText.setEnabled(True)
                # filterKeywordText["bg"] = "SystemWindow"
                # filterKeywordText["fg"] = "SystemWindowText"
                # endKeywordEntry["state"] = "normal"
                self.ui.endKeywordEntry.setEnabled(True)
                # configButton["state"] = "normal"
                self.ui.configButton.setEnabled(True)
                # readImagesDirButton["state"] = "normal"
                self.ui.readImagesDirButton.setEnabled(True)
                # readLogDirButton["state"] = "normal"
                self.ui.readLogDirButton.setEnabled(True)
                # outputDirButton["state"] = "normal"
                self.ui.outputDirButton.setEnabled(True)
                # executeParserButton["state"] = "normal"
                self.ui.executeParserButton.setEnabled(True)
                # executeParserButton["text"] = "執行"
                self.ui.executeParserButton.setText("執行")
                # executeParserProgressBar.grid_forget()
                self.ui.executeParserProgressBar.hide()
                # statusLabel["text"] = "處理完成。"
                self.ui.statusLabel.setText("處理完成。")
                break

    def executeParser(self):
        # global CONFIG_FOLDER, PROJECT_NAME, LOG_DIR, PHOTO_DIR
        # statusLabel["text"] = ""
        self.ui.statusLabel.setText("")
        if os.path.isdir(self.PHOTO_DIR) and os.path.isdir(self.LOG_DIR) and os.path.isdir(self.OUTPUT_DIR) and os.path.exists(self.CONFIG_FOLDER + self.PROJECT_NAME + ".json"):
            print("status ok.")
            
            parser = main_UIParser.UIParser(self.LOG_DIR + "\\", self.PHOTO_DIR + "\\", self.OUTPUT_DIR + "\\", self.CONFIG_FOLDER, self.PROJECT_NAME)
            
            UIparserThread = threading.Thread(target = parser.executeUIParser)
            UIparserThread.daemon = True #cannot actually stop this thread when exit window
            UIparserThread.start()
            
            progressThread = threading.Thread(target = self.executeProgress, args = (parser,))
            progressThread.daemon = True
            progressThread.start()
        
    
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())