# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:37:27 2023

@author: StevenSSLin
"""
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import os
import json
import main_UIParser
import threading
import time


#global variable
CONFIG_FOLDER = "config\\"
PHOTO_DIR = ""
LOG_DIR = ""
OUTPUT_DIR = ""
PROJECT_NAME = ""
isConfig = False

#main window settings
mainWindow = tk.Tk()
mainWindow.title('AF log parser V4.1')
mainWindow.geometry('420x600')
mainWindow.resizable(False, False)


#function setup

def detectParserReady():
    global isConfig, PHOTO_DIR, LOG_DIR, OUTPUT_DIR
    if isConfig and PHOTO_DIR != "" and LOG_DIR != "" and OUTPUT_DIR != "":
        executeParserButton["state"] = tk.NORMAL
    else:
        executeParserButton["state"] = tk.DISABLED

def showPhotoFileDialog():
    global PHOTO_DIR
    PHOTO_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇圖片資料夾")
    readImagesDirLabel["text"] = PHOTO_DIR
    detectParserReady()
    
def showLogFileDialog():
    global LOG_DIR
    LOG_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇log資料夾")
    readLogDirLabel["text"] = LOG_DIR
    detectParserReady()

def showOutputFileDialog():
    global OUTPUT_DIR
    OUTPUT_DIR = filedialog.askdirectory(initialdir=r"C:\\", title="選擇匯出資料夾")
    outputDirLabel["text"] = OUTPUT_DIR
    detectParserReady()


def writeNewConfig():
    global PROJECT_NAME, isConfig
    #set all label bg color as default
    projectNameLabel.config(bg = 'SystemButtonFace')
    filterKeywordLabel.config(bg = 'SystemButtonFace')
    endKeywordLabel.config(bg = 'SystemButtonFace')
    
    if projectNameEntry.get() == "":
        projectNameLabel.config(bg = "red")
        configStatusLabel["text"] = "部分欄位為空，請重新設定"
    if filterKeywordText.get(1.0, 'end-1c') == "":
        filterKeywordLabel.config(bg = "red")
        configStatusLabel["text"] = "部分欄位為空，請重新設定"
    if endKeywordEntry.get() == "":
        endKeywordLabel.config(bg = "red")
        configStatusLabel["text"] = "部分欄位為空，請重新設定"
    
    if projectNameEntry.get() != "" and filterKeywordText.get(1.0, 'end-1c') != "" and endKeywordEntry.get() != "":
        PROJECT_NAME = projectNameEntry.get()
        
        writeConfigs = dict()
        
        writeConfigs["project_name"] = projectNameEntry.get()
        writeConfigs["previous_second_to_start_log"] = int(prevSecClipSpinbox.get())
        
        filterKeywordList = []
        for i in range(len(filterKeywordText.get(1.0, 'end-1c').split("\n"))):
            if filterKeywordText.get(1.0, 'end-1c').split("\n")[i] == "":
                continue
            else:
                filterKeywordList.append(filterKeywordText.get(1.0, 'end-1c').split("\n")[i])
        writeConfigs["log_keyword"] = filterKeywordList
        
        writeConfigs["save_keyword"] = [endKeywordEntry.get()]
        
        with open(CONFIG_FOLDER + projectNameEntry.get() + ".json", 'w') as outFile:
            json.dump(writeConfigs, outFile, indent = 4)
        configStatusLabel["text"] = "設定檔寫入完成!"
        isConfig = True
        detectParserReady()

def stateUpdate(event):
    global PROJECT_NAME, isConfig
    PROJECT_NAME = ""
    statusLabel["text"] = ""
    if len(projectNameEntry.get()) == 0:
        configButton["state"] = tk.DISABLED
        filterKeywordText.delete(1.0, 'end-1c')
        endKeywordEntry.delete(0, tk.END)
    else:
        configButton["state"] = tk.NORMAL
    
    configStatusLabel["text"] = "請先填入專案名稱與相關設定"
    config_files = os.listdir(CONFIG_FOLDER)
    isConfig = False
    detectParserReady()

    for config_file in config_files:
        config_file_name = config_file.split(".")[0]        
        if projectNameEntry.get() == config_file_name:
            #有匹配到就使用配置檔的設定，並在更新狀態顯示
            configStatusLabel["text"] = "已有該專案配置檔"
            PROJECT_NAME = config_file_name
            with open(CONFIG_FOLDER + config_file) as jsonFile:
                config = json.load(jsonFile)
            
            defaultPrevSec.set(config["previous_second_to_start_log"])
            
            filterKeywordText.delete(1.0, 'end-1c')

            for i in range(len(config["log_keyword"])):
                if i == len(config["log_keyword"]) - 1:
                    filterKeywordText.insert(tk.INSERT, str(config["log_keyword"][i]))
                else:
                    filterKeywordText.insert(tk.INSERT, str(config["log_keyword"][i]) + '\n')
            
            endKeywordEntry.delete(0, tk.END)
            endKeywordEntry.insert(0, str(config["save_keyword"][0]))
            isConfig = True
            detectParserReady()
            break

def executeProgress(parser):
    #block all user-type widget when parsing logs
    projectNameEntry["state"] = "disable"
    prevSecClipSpinbox["state"] = "disable"
    filterKeywordText["state"] = "disable"
    filterKeywordText["bg"] = "#F0F0F0"
    filterKeywordText["fg"] = "#777777"
    endKeywordEntry["state"] = "disable"
    configButton["state"] = "disable"
    readImagesDirButton["state"] = "disable"
    readLogDirButton["state"] = "disable"
    outputDirButton["state"] = "disable"
    executeParserButton["state"] = "disable"
    executeParserButton["text"] = "Log解析中"
    executeParserProgressBar.grid(row = 12, column = 0, pady = 5, columnspan=2)
    
    prev = 0
    executeParserProgressBar["value"] = prev
    i=0
    while(True):
        #config UI when parse error
        if parser.isParseError:
            tk.messagebox.showwarning("解析錯誤", parser.parseErrorMessage)
            projectNameEntry["state"] = "normal"
            prevSecClipSpinbox["state"] = "normal"
            filterKeywordText["state"] = "normal"
            filterKeywordText["bg"] = "SystemWindow"
            filterKeywordText["fg"] = "SystemWindowText"
            endKeywordEntry["state"] = "normal"
            configButton["state"] = "normal"
            readImagesDirButton["state"] = "normal"
            readLogDirButton["state"] = "normal"
            outputDirButton["state"] = "normal"
            executeParserButton["state"] = "normal"
            executeParserButton["text"] = "執行"
            executeParserProgressBar.grid_forget()
            break
        
        #update progress bar
        time.sleep(0.001) #do not modify. Remove this line will cause stuck, set longer will make warning message not pop up.
        progressAtWork = int(parser.currentProcessPhotoNum / parser.totalPhotoNum * 100)
        if prev != progressAtWork:
            for i in range(prev, progressAtWork+1):
                time.sleep(0.001) #shorter makes progress update more frequently
                executeParserProgressBar["value"] = i
            prev = progressAtWork
        
        #update status when parsing
        statusLabel["text"] = "".join(parser.parseState)
        
        #log parse complete
        if parser.currentProcessPhotoNum == parser.totalPhotoNum:
            projectNameEntry["state"] = "normal"
            prevSecClipSpinbox["state"] = "normal"
            filterKeywordText["state"] = "normal"
            filterKeywordText["bg"] = "SystemWindow"
            filterKeywordText["fg"] = "SystemWindowText"
            endKeywordEntry["state"] = "normal"
            configButton["state"] = "normal"
            readImagesDirButton["state"] = "normal"
            readLogDirButton["state"] = "normal"
            outputDirButton["state"] = "normal"
            executeParserButton["state"] = "normal"
            executeParserButton["text"] = "執行"
            executeParserProgressBar.grid_forget()
            statusLabel["text"] = "處理完成。"
            break

def executeParser():
    global CONFIG_FOLDER, PROJECT_NAME, LOG_DIR, PHOTO_DIR
    statusLabel["text"] = ""
    if os.path.isdir(PHOTO_DIR) and os.path.isdir(LOG_DIR) and os.path.isdir(OUTPUT_DIR) and os.path.exists(CONFIG_FOLDER + PROJECT_NAME + ".json"):
        print("status ok.")
        
        parser = main_UIParser.UIParser(LOG_DIR + "\\", PHOTO_DIR + "\\", OUTPUT_DIR + "\\", CONFIG_FOLDER, PROJECT_NAME)
        
        UIparserThread = threading.Thread(target = parser.executeUIParser)
        UIparserThread.daemon = True #cannot actually stop this thread when exit window
        UIparserThread.start()
        
        progressThread = threading.Thread(target = executeProgress, args = (parser,))
        progressThread.daemon = True
        progressThread.start()
        

#function UI setup
projectNameLabel = tk.Label(mainWindow, text = "專案名稱:")
projectNameEntry = tk.Entry(mainWindow)#使用者輸入框
prevSecClipLabel = tk.Label(mainWindow, text = "首張照片擷取前幾秒:")
defaultPrevSec = tk.IntVar(mainWindow)
defaultPrevSec.set(3)
prevSecClipSpinbox = tk.Spinbox(mainWindow, from_ = 1, to = 5, textvariable = defaultPrevSec, state = 'readonly')
filterKeywordLabel = tk.Label(mainWindow, text = "欲篩選關鍵字:")
filterKeywordText = tk.Text(mainWindow, width = 26, height = 2)
endKeywordLabel = tk.Label(mainWindow, text = "欲結束關鍵字:")
endKeywordEntry = tk.Entry(mainWindow)
configButton = tk.Button(mainWindow, text = "寫入設定檔", command = writeNewConfig, state = tk.DISABLED)
configStatusLabel = tk.Label(mainWindow, text = "請先填入專案名稱與相關設定", font=('Helvetica', 12, 'bold'))
readImagesDirButton = tk.Button(mainWindow, text = "選擇 圖片 資料夾", command = showPhotoFileDialog)
readImagesDirLabel = tk.Label(mainWindow, width = 30, wraplength = 200, justify = "left")
readLogDirButton = tk.Button(mainWindow, text = "選擇 log 資料夾", command = showLogFileDialog)
readLogDirLabel = tk.Label(mainWindow, width = 30, wraplength = 200, justify = "left")
outputDirButton = tk.Button(mainWindow, text = "選擇 匯出 資料夾", command = showOutputFileDialog)
outputDirLabel = tk.Label(mainWindow, width = 30, wraplength = 200, justify = "left")
executeParserButton = tk.Button(mainWindow, text = "執行", font=('Helvetica', 12, 'bold'), command = executeParser, state = tk.DISABLED)
executeParserProgressBar = ttk.Progressbar(mainWindow, length = 350)
statusLabel = tk.Label(mainWindow, text = "")


#UI constraint setup
projectNameLabel.grid(row = 0, column = 0, padx = 5, pady = (30, 5))
projectNameEntry.grid(row = 0, column = 1, ipadx = 20, pady = (30, 5))
prevSecClipLabel.grid(row = 1, column = 0, padx = 5)
prevSecClipSpinbox.grid(row = 1, column = 1, ipadx = 0)
filterKeywordLabel.grid(row = 2, column = 0, padx = 5)
filterKeywordText.grid(row = 2, column = 1, columnspan=2, padx = (5, 5), pady = 5) #0301
endKeywordLabel.grid(row = 3, column = 0, padx = 5)
endKeywordEntry.grid(row = 3, column = 1, ipadx = 20)
configStatusLabel.grid(row = 4, column = 0, pady = 5, ipadx = 80, ipady = 2, columnspan=2)
configButton.grid(row = 5, column = 0, pady = (5, 30), ipadx = 150, ipady = 2, columnspan=2)
readImagesDirButton.grid(row = 6, column = 0, pady = 5, ipadx = 30, ipady = 2)
readImagesDirLabel.grid(row = 6, column = 1, pady = 5, ipadx = 10, ipady = 2)
readLogDirButton.grid(row = 7, column = 0, pady = 5, ipadx = 30, ipady = 2)
readLogDirLabel.grid(row = 7, column = 1, pady = 5, ipadx = 10, ipady = 2)
outputDirButton.grid(row = 8, column = 0, pady = 5, ipadx = 30, ipady = 2)
outputDirLabel.grid(row = 8, column = 1, pady = 5, ipadx = 10, ipady = 2)
executeParserButton.grid(row = 9, column = 0, pady = (15, 5), ipadx = 140, ipady = 2, columnspan=2)
statusLabel.grid(row = 10, column = 0, pady = 5, ipady = 2, columnspan=2)
executeParserProgressBar.grid(row = 11, column = 0, pady = 5, columnspan=2)
executeParserProgressBar.grid_forget()


#callback event setup
projectNameEntry.bind('<KeyRelease>', stateUpdate)



mainWindow.mainloop()