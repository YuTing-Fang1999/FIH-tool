from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import os
import json
from QC.AF import main_UIParser
import threading
import time

class MyWidget(ParentWidget):
    update_executeParser_state_signal = pyqtSignal(str)   
    update_statusLabel_signal = pyqtSignal(str)
    update_executeParserProgressBar_signal = pyqtSignal(int)
    show_error_message_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.executeParserProgressBar.hide()
        self.ui.prevSecClipSpinbox.wheelEvent = lambda e: e.ignore()
        self.ui.prevSecClipSpinbox.lineEdit().setReadOnly(True)
        
        #global variable
        self.CONFIG_FOLDER = "QC\\AF\\config\\"
        self.PHOTO_DIR = ""
        self.LOG_DIR = ""
        self.OUTPUT_DIR = ""
        self.PROJECT_NAME = ""
        self.isConfig = False
        
        self.controller()
        self.stateUpdate("")
        self.detectParserReady()

    def controller(self):
        self.ui.configButton.clicked.connect(self.writeNewConfig)
        self.ui.readImagesDirButton.clicked.connect(self.showPhotoFileDialog)
        self.ui.readLogDirButton.clicked.connect(self.showLogFileDialog)
        self.ui.outputDirButton.clicked.connect(self.showOutputFileDialog)
        self.ui.executeParserButton.clicked.connect(self.executeParser)
        
        self.ui.projectNameEntry.textChanged.connect(self.stateUpdate)
        self.update_executeParser_state_signal.connect(self.update_executeParser_state)
        self.update_executeParserProgressBar_signal.connect(self.update_executeParserProgressBar)
        self.update_statusLabel_signal.connect(self.update_statusLabel)
        self.show_error_message_signal.connect(self.show_error_message)
        
    def show_error_message(self, message):
        QMessageBox.about(self, "解析錯誤", message)
        
    def set_btn_enable(self, b):
        if b:
            style =  "QPushButton {background:rgb(248, 203, 173); color: black;}"
        else:
            style =  "QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
        
        # projectNameEntry["state"] = "disable"
        self.ui.projectNameEntry.setEnabled(b)
        # prevSecClipSpinbox["state"] = "disable"
        self.ui.prevSecClipSpinbox.setEnabled(b)
        # filterKeywordText["state"] = "disable"
        self.ui.filterKeywordText.setEnabled(b)
        # filterKeywordText["bg"] = "#F0F0F0"
        # filterKeywordText["fg"] = "#777777"
        # endKeywordEntry["state"] = "disable"
        self.ui.endKeywordEntry.setEnabled(b)
        # configButton["state"] = "disable"
        self.ui.configButton.setEnabled(b)
        self.ui.configButton.setStyleSheet(style)
        # readImagesDirButton["state"] = "disable"
        self.ui.readImagesDirButton.setEnabled(b)
        self.ui.readImagesDirButton.setStyleSheet(style)
        # readLogDirButton["state"] = "disable"
        self.ui.readLogDirButton.setEnabled(b)
        self.ui.readLogDirButton.setStyleSheet(style)
        # outputDirButton["state"] = "disable"
        self.ui.outputDirButton.setEnabled(b)
        self.ui.outputDirButton.setStyleSheet(style)
        # executeParserButton["state"] = "disable"
        self.ui.executeParserButton.setEnabled(b)
        self.ui.executeParserButton.setStyleSheet(style)
        
    def update_executeParser_state(self, text):
        if text == "Log解析中":
            #block all user-type widget when parsing logs
            self.set_btn_enable(False)
            # executeParserButton["text"] = "Log解析中"
            self.ui.executeParserButton.setText("Log解析中")
            # executeParserProgressBar.grid(row = 12, column = 0, pady = 5, columnspan=2)
            self.ui.executeParserProgressBar.show()
        elif text == "解析錯誤":
            # tk.messagebox.showwarning("解析錯誤", parser.parseErrorMessage)
            self.set_btn_enable(True)
            # executeParserButton["text"] = "執行"
            self.ui.executeParserButton.setText("執行(QC)")
            # executeParserProgressBar.grid_forget()
            self.ui.executeParserProgressBar.hide()
        elif text == "處理完成":
            self.set_btn_enable(True)
            # executeParserButton["text"] = "執行"
            self.ui.executeParserButton.setText("執行(QC)")
            # executeParserProgressBar.grid_forget()
            self.ui.executeParserProgressBar.hide()
            # statusLabel["text"] = "處理完成。"
            self.ui.statusLabel.setText("處理完成。")
        else:
            self.ui.statusLabel.setText("ERROR")
            
    
    def update_executeParserProgressBar(self, value):
        self.ui.executeParserProgressBar.setValue(value)
        
    def update_statusLabel(self, text):
        self.ui.statusLabel.setText(text)
        
    #function setup
    def detectParserReady(self):
        if self.isConfig and self.PHOTO_DIR != "" and self.LOG_DIR != "" and self.OUTPUT_DIR != "":
            self.ui.executeParserButton.setEnabled(True)
            self.ui.executeParserButton.setStyleSheet("QPushButton {background:rgb(248, 203, 173); color: black;}")
            # executeParserButton["state"] = tk.NORMAL
        else:
            self.ui.executeParserButton.setEnabled(False)
            self.ui.executeParserButton.setStyleSheet("QPushButton {background: rgb(150, 150, 150); color: rgb(100, 100, 100);}")
            # executeParserButton["state"] = tk.DISABLED

    def showPhotoFileDialog(self):
        # global PHOTO_DIR
        # PHOTO_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇圖片資料夾")
        # readImagesDirLabel["text"] = PHOTO_DIR
        # detectParserReady()
        
        # Open file dialog
        self.PHOTO_DIR = QFileDialog.getExistingDirectory(self,"選擇圖片資料夾", self.get_path("QUL_AF_folder"))
        if self.PHOTO_DIR == "": return
        self.ui.readImagesDirLabel.setText(self.PHOTO_DIR)
        self.set_path('QUL_AF_folder', '/'.join(self.PHOTO_DIR.split('/')[:-1]))
        self.detectParserReady()
        
        self.ui.photo_list_label.setText("")
        for f in os.listdir(self.PHOTO_DIR):
            self.ui.photo_list_label.setText(self.ui.photo_list_label.text() + f + '\n')
        
    def showLogFileDialog(self):
        # global LOG_DIR
        # LOG_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇log資料夾")
        # readLogDirLabel["text"] = LOG_DIR
        # detectParserReady()
        
        # Open file dialog
        self.LOG_DIR = QFileDialog.getExistingDirectory(self,"選擇log資料夾", self.get_path("QUL_AF_folder"))
        if self.LOG_DIR == "": return
        self.ui.readLogDirLabel.setText(self.LOG_DIR)
        self.set_path('QUL_AF_folder', '/'.join(self.LOG_DIR.split('/')[:-1]))
        self.detectParserReady()
        
        self.ui.log_list_label.setText("")
        not_alog = True
        for f in os.listdir(self.LOG_DIR):
            if "alog" in f:
                not_alog = False
            self.ui.log_list_label.setText(self.ui.log_list_label.text() + f + '\n')
            
        if not_alog:
            QMessageBox.about(self, "Log資料夾錯誤", "QC的log通常以alog開頭，請確認是否選到錯誤的資料夾")

    def showOutputFileDialog(self):
        # global OUTPUT_DIR
        # OUTPUT_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇匯出資料夾")
        # outputDirLabel["text"] = OUTPUT_DIR
        # detectParserReady()
        
        # Open file dialog
        self.OUTPUT_DIR = QFileDialog.getExistingDirectory(self,"選擇匯出資料夾", '/'.join(self.get_path("QUL_AF_output_folder").split('/')[:-1]))
        if self.OUTPUT_DIR == "": return
        self.ui.outputDirLabel.setText(self.OUTPUT_DIR)
        self.set_path('QUL_AF_output_folder', self.OUTPUT_DIR)
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
            self.ui.configButton.setStyleSheet("QPushButton {background:rgb(150, 150, 150); color: rgb(100, 100, 100);}")
            # filterKeywordText.delete(1.0, 'end-1c')
            # endKeywordEntry.delete(0, tk.END)
            self.ui.filterKeywordText.setText("")
            self.ui.endKeywordEntry.setText("")
        else:
            # configButton["state"] = tk.NORMAL
            self.ui.configButton.setEnabled(True)
            self.ui.configButton.setStyleSheet("background:rgb(248, 203, 173); color: black;")
        
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
        print("executeProgress")
        self.update_executeParser_state_signal.emit("Log解析中")
        
        prev = 0
        # executeParserProgressBar["value"] = prev
        # self.ui.executeParserProgressBar.setValue(prev)
        self.update_executeParserProgressBar_signal.emit(prev)
        i=0
        while(True):
            #config UI when parse error
            if parser.isParseError:
                self.update_executeParser_state_signal.emit("解析錯誤")
                self.show_error_message_signal.emit(parser.parseErrorMessage)
                break

            if parser.isPrecheckError:
                self.update_executeParser_state_signal.emit("處理完成")
            
            #update progress bar
            time.sleep(0.001) #do not modify. Remove this line will cause stuck, set longer will make warning message not pop up.
            progressAtWork = int(parser.currentProcessPhotoNum / parser.totalPhotoNum * 100)
            if prev != progressAtWork:
                for i in range(prev, progressAtWork+1):
                    time.sleep(0.001) #shorter makes progress update more frequently
                    # executeParserProgressBar["value"] = i
                    # self.ui.executeParserProgressBar.setValue(i)
                    self.update_executeParserProgressBar_signal.emit(i)
                prev = progressAtWork
            
            #update status when parsing
            # statusLabel["text"] = "".join(parser.parseState)
            # self.ui.statusLabel.setText("".join(parser.parseState))
            self.update_statusLabel_signal.emit("".join(parser.parseState))
            
            #log parse complete
            if parser.currentProcessPhotoNum == parser.totalPhotoNum:
                self.update_executeParser_state_signal.emit("處理完成")
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
            
            progressThread = threading.Thread(target = self.executeProgress, args=(parser,))
            progressThread.daemon = True
            progressThread.start()
        
    
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())