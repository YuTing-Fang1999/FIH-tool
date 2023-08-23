# -*- coding: utf-8 -*-
"""
Created on Wed Dec  21 9:50:25 2022

@author: StevenSSLin
"""
import json
import os, shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

class UIParser():
    def __init__(self, inputLogPath, inputPhotoPath, outputPath, configFolder, projectName):
        self.platform = "MTK" #switch by platform. valid values are ["QC", "MTK"]
        self.logCheckKeyword = ""
        self.inputLogPath = inputLogPath
        self.inputPhotoPath = inputPhotoPath
        self.outputPath = outputPath
        self.configFolder = configFolder
        self.projectName = projectName
        self.allUpdatedLogsFileName = []
        self.startLogSearchingFileIdx = 0
        self.lastTimeEndWriteLogLinesIdx = -1
        self.currentPhotoHour = 0
        self.currentPhotoMinute = 0
        self.currentPhotoSecond = 0
        self.savedLogForCurrentPhotoStage1 = []
        self.savedLogForCurrentPhotoStage2 = []
        self.losslogRecordStage1 = []
        self.exportEmptyLog = False
        self.stage1captureTimestampFileIdx = 0
        self.stage1captureTimestampLogLinesIdx = -1
        self.currentProcessPhotoNum = 0
        self.totalPhotoNum = len(os.listdir(inputPhotoPath))
        self.isParseError = False
        self.isPrecheckError = False
        self.parseErrorMessage = "解析錯誤。請確認資料夾是否有照片和log；或是有遺失log，導致解析不完全。"
        self.parseState = ""
    
    def executeUIParser(self):
        if self.isPhotoAndLogInTheFolder():
            configSettings = self.readConfigFile(self.configFolder, self.projectName)
            
            self.clearPrevOutputFolder(self.outputPath)
            
            if self.platform == "QC":
                self.processOfflineLogFileExtensionQC(self.inputLogPath)
            elif self.platform == "MTK":
                self.processOfflineLogFileExtensionMTK(self.inputLogPath)
         
            for i in range(self.totalPhotoNum):
                currentProcessPhotoName = os.listdir(self.inputPhotoPath)[i]
                
                self.currentProcessPhotoNum += 1
                print("Now processing: ", currentProcessPhotoName, "'s log.")
                self.parseState = "正在處理 ", currentProcessPhotoName, "的 log。"
                if i == 0:
                    #is first photo
                    isFirstPhoto = True
                    self.processPhoto(self.inputPhotoPath, currentProcessPhotoName, isFirstPhoto, configSettings)
                else:
                    #the rest photo
                    isFirstPhoto = False
                    self.processPhoto(self.inputPhotoPath, currentProcessPhotoName, isFirstPhoto, configSettings)
            print("Log parse complete.")
            self.parseState = "Log 解析完成。"
        else:
            self.isParseError = True
            print("Please refer to the error message and re-run the program. Press Enter to continue...")
            self.parseState = "請參考錯誤訊息，並重新執行一次。"



    def isRequiredPathExist(self):
        if (os.path.exists(self.inputLogPath) and os.path.exists(self.inputPhotoPath) and os.path.exists(self.outputPath)):
            return True
        
        if not os.path.exists(self.inputLogPath):
            os.mkdir(self.inputLogPath)
            print("input log path not exist, please put offline logs to the \"0_input_log\" folders. Press Enter to continue...")
        if not os.path.exists(self.inputPhotoPath):
            os.mkdir(self.inputPhotoPath)
            print("input photo path not exist, please put photos to the \"0_input_photo\" folders. Press Enter to continue...")
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
            print("output log path not exist, creating the \"1_output\" folders. Press Enter to continue...")
        return False
    
    def isPhotoAndLogInTheFolder(self):
        if len(os.listdir(self.inputPhotoPath)) > 0 and len(os.listdir(self.inputLogPath)) > 0:
            if self.platform == "QC":
                self.logCheckKeyword = "alog"
            elif self.platform == "MTK":
                self.logCheckKeyword = "main_log"
            print("Precheck log with valid keyword: ", self.logCheckKeyword)
            if any(self.logCheckKeyword in fileName for fileName in os.listdir(self.inputLogPath)):
                print("contain valid log, continue analysis")
                return True
            else:
                print("log does not contain valid name")
                self.isPrecheckError = True
                self.parseErrorMessage = "log 資料夾內沒有帶" + self.logCheckKeyword + "字眼的檔案，請確認log是否有放錯。"
                return False
        elif len(os.listdir(self.inputPhotoPath)) == 0 and len(os.listdir(self.inputLogPath)) > 0:
            print("No photo in the \"0_input_photo\" folders. Press Enter to continue...")
            self.isPrecheckError = True
            self.parseErrorMessage = "圖片 資料夾內沒有照片。"
        elif len(os.listdir(self.inputPhotoPath)) > 0 and len(os.listdir(self.inputLogPath)) == 0:
            print("No log in the \"0_input_log\" folders. Press Enter to continue...")
            self.isPrecheckError = True
            self.parseErrorMessage = "log 資料夾內沒有log檔案。"
        else:
            print("No log and photo in the \"0_input_log\" and \"0_input_photo\" folders. Press Enter to continue...")
            self.isPrecheckError = True
            self.parseErrorMessage = "圖片 資料夾 和 log 資料夾內沒有檔案。"
        return False
        
    def clearPrevOutputFolder(self, outputPath):
        if len(os.listdir(outputPath)) > 0:
            shutil.rmtree(outputPath, ignore_errors=True)
            os.mkdir(outputPath)
    
    def processOfflineLogFileExtensionQC(self, inputLogPath):
        #remove unwnated log files
        for file in os.listdir(inputLogPath):
            if file.startswith("alog_"):
                os.remove(inputLogPath + file)
        #rename log with .txt extension
        originalLogs = sorted(os.listdir(inputLogPath), reverse = True)
    
        for logName in originalLogs:
            if logName.split(".")[-1] != "txt":
                if logName == "alog":
                    os.rename(inputLogPath + logName, inputLogPath + logName + ".000.txt")
                else:
                    os.rename(inputLogPath + logName, inputLogPath + logName + ".txt")

        self.allUpdatedLogsFileName= sorted(os.listdir(inputLogPath), reverse = True)
    
    def processOfflineLogFileExtensionMTK(self, inputLogPath):
        #leave used log
        for file in os.listdir(inputLogPath):
            if not file.startswith("main_log"):
                os.remove(inputLogPath + file)
        #rename main_log with .txt extension
        for logName in os.listdir(inputLogPath):
            if logName.split(".")[-1] != "txt":
                os.rename(inputLogPath + logName, inputLogPath + logName + ".txt")
        # METHOD1: sorted log files by modified datetime
        # logFilesContainDatetime = []
        # for fileName in os.listdir(inputLogPath):
        #     datetimeObj = datetime.datetime.strptime(datetime.datetime.fromtimestamp(os.path.getmtime(inputLogPath + fileName)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        #     logFilesContainDatetime.append({'logname': fileName, 'logModTime' : datetimeObj})
        # sortedLogFilesByModTime = sorted(logFilesContainDatetime, key = lambda x : x['logModTime'])
        # sortedOnlyLogFileName = [logFile['logname'] for logFile in sortedLogFilesByModTime]
        # self.allUpdatedLogsFileName = sortedOnlyLogFileName
        # print("sorted log:")
        # print(self.allUpdatedLogsFileName)
        
        
        # METHOD2: sorted log files by main_log naming index
        # {key : value} = {檔名 : 檔名數字}，透過value的檔名數字做排序
        sortedLogFileName = []
        tempLogFile = dict()
        for fileName in os.listdir(inputLogPath):
            startCharacterIndex = 9
            endFilterKeyword = "__"  #根據數字後面的2個下底線作為數字擷取的標記
            endCharacterIndex = fileName.find(endFilterKeyword)
            indexNumOfLogFile = int(fileName[startCharacterIndex : endCharacterIndex])
            tempLogFile[fileName] = indexNumOfLogFile
        
        tempSortedLogFiles = sorted(tempLogFile.items(), key=lambda item: item[1])
        for (k, v) in tempSortedLogFiles:
            sortedLogFileName.append(k)
        self.allUpdatedLogsFileName = sortedLogFileName
        print("Log will start to search one by one as follows:")
        print(self.allUpdatedLogsFileName)
        
    
    def writeLogContent(self, outputPath, photoName, logContentToWrite):
        with open(outputPath + photoName + ".txt", 'w', newline = '', encoding='UTF-8') as newLogFile:
            for line in logContentToWrite:
                newLogFile.write("%s" % line)
            print(photoName + "'s log is saved.")
            newLogFile.close()
            
    def copyPhotoToOutputFolder(self, inputPhotoPath, photoName, outputPath):
        shutil.copy(os.path.join(inputPhotoPath, photoName), outputPath)
    
    def containKeywords(self, log, keywordlist):
        if any(x in log for x in keywordlist):
            return True
        else:
            return False
    
    def fetchLogContent(self, photoName, isFirstPhoto, prevNsecHour, prevNsecMinute, prevNsecSecond, after3secPhotoHour, after3secPhotoMinute, after3secPhotoSecond, logRecordKeyword, saveKeyword):
        #避免照片沒有在所有的log被紀錄，然後搜尋完整份log的index會跑到最後一份log。若下一張照片的資訊有存在log，就會因為log搜尋index已到底，而被當成是沒有紀錄到log
        if self.startLogSearchingFileIdx == len(self.allUpdatedLogsFileName):
            print("index reach MAXIMUM log length, ", self.startLogSearchingFileIdx)
            self.startLogSearchingFileIdx = 0
        
        tempAllLines = []
        self.savedLogForCurrentPhotoStage1 = []
        if self.exportEmptyLog:
            self.exportEmptyLog = False
        
        isFindFirstLine = False if isFirstPhoto else True #flag to set if it is the starting point to record log for the current photo
        isNotReadyToLogNextPhoto = True
        isFindCaptureTimestamp = False
        
        isNeedEnterStage2 = True
        stage2NotFoundSavePhotoLogPosition = False
        isPhotoLogIncludeInLog = False
        self.isParseError = False
        
        ### Stage 1 ###
        while(isNotReadyToLogNextPhoto):
            if self.startLogSearchingFileIdx >= len(self.allUpdatedLogsFileName):
                print("Search at the end of the last log, possibily due to loss log for this photo. Press Enter to continue...")
                self.isParseError = True
                self.parseErrorMessage = "照片: " + photoName + " 未找到對應的log片段，可能有掉log的問題存在。"
                isNeedEnterStage2 = False
                self.exportEmptyLog = True
                #log index out of bounds
                break
            with open(self.inputLogPath + self.allUpdatedLogsFileName[self.startLogSearchingFileIdx], 'r', encoding="utf-8") as f:
                print("Now process log: ", self.allUpdatedLogsFileName[self.startLogSearchingFileIdx])
                lines = f.readlines()
                f.close()
                #In v9.3, if NUL characters saved in large text file, it will cause iostream time out problem.
                #below code will replace NUL to empty character and remove empty line cause by eliminate NUL characters
                removeNULLines = [line.replace('\0', '') for line in lines]
                while ("" in removeNULLines):
                    removeNULLines.remove("")
                ### save log without NUL characters
                for line in removeNULLines:
                    tempAllLines.append(line)
            for idx, oneline in enumerate(tempAllLines):
                if isFindCaptureTimestamp:
                    break
                if (not isFirstPhoto and self.lastTimeEndWriteLogLinesIdx >= idx) or oneline.startswith("-"):
                    continue
                oneline_split_hour = int(oneline.split(" ")[1].split(":")[0])
                oneline_split_minute = int(oneline.split(" ")[1].split(":")[1])
                oneline_split_second = int(oneline.split(" ")[1].split(":")[2].split(".")[0])
                
                #如果第1張照片的EXIF時間前N秒比log最早的紀錄時間還要晚，代表照片的時序資訊一定會紀錄在log裡
                if isFirstPhoto and (prevNsecHour >= oneline_split_hour) and (prevNsecMinute >= oneline_split_minute) and (prevNsecSecond >= oneline_split_second):
                    isPhotoLogIncludeInLog = True
                
                #如果第1張照片的EXIF時間前N秒比log最早的紀錄時間還要早，而且isPhotoLogIncludeInLog被標示為False，代表照片的時序資訊沒有完整被log紀錄，或是都沒被log記錄到
                if isFirstPhoto and (prevNsecHour <= oneline_split_hour) and (prevNsecMinute <= oneline_split_minute) and (prevNsecSecond <= oneline_split_second) and not isPhotoLogIncludeInLog:
                    print("WARNING: The information of this photo is not fully recorded in the log file. Export empty log file.")
                    self.lastTimeEndWriteLogLinesIdx = -1
                    isNotReadyToLogNextPhoto = False
                    isNeedEnterStage2 = False
                    stage2NotFoundSavePhotoLogPosition = True
                    self.exportEmptyLog = True
                    self.isParseError = True
                    self.parseErrorMessage = "log可能沒有完整記錄到照片: " + photoName + " 的前期資訊。"
                    break
                
                #第1張
                if isFirstPhoto and oneline_split_hour == prevNsecHour and oneline_split_minute == prevNsecMinute and oneline_split_second == prevNsecSecond \
                    and not isFindFirstLine and self.containKeywords(oneline, logRecordKeyword):
                    #the current line is the start position to record log
                    print("The current line %d of log %s is the start position to record log" % (idx + 1, self.allUpdatedLogsFileName[self.startLogSearchingFileIdx]))
                    isFindFirstLine = True
                    
                #紀錄這張照片的EXIF時間戳，在哪一份log的哪一行
                if oneline_split_hour == currentPhotoHour and oneline_split_minute == currentPhotoMinute and oneline_split_second == currentPhotoSecond:
                    self.stage1captureTimestampFileIdx = self.startLogSearchingFileIdx
                    self.stage1captureTimestampLogLinesIdx = idx - 1
                    self.lastTimeEndWriteLogLinesIdx = idx - 1 #stage 2會從這行繼續搜尋
                    print("Get photo timestamp log, go to stage 2.")
                    isNotReadyToLogNextPhoto = False
                    break
                    

                #若saveKeyword在EXIF time之前就已經出現，而且saveKeyword落在前N秒跟後N秒之間，足以代表這個keyword就是專屬這張照片的log
                prevTime = datetime.time(int(prevNsecHour), int(prevNsecMinute), int(prevNsecSecond))
                currTime = datetime.time(int(oneline_split_hour), int(oneline_split_minute), int(oneline_split_second))
                afterTime = datetime.time(int(after3secPhotoHour), int(after3secPhotoMinute), int(after3secPhotoSecond))
                
                if self.containKeywords(oneline, saveKeyword) and prevTime < currTime < afterTime:
                    print("Save keyword appears before the EXIF time. Skip stage 2.")
                    self.savedLogForCurrentPhotoStage1.append(oneline)
                    self.lastTimeEndWriteLogLinesIdx = idx #下一張照片從這行繼續搜尋
                    isNotReadyToLogNextPhoto = False
                    isNeedEnterStage2 = False
                    stage2NotFoundSavePhotoLogPosition = True
                    break
                

                #當前行數有要記錄的關鍵字並且已經有起始flag位置
                if self.containKeywords(oneline, logRecordKeyword) and isFindFirstLine:
                    #append oneline to output log
                    self.savedLogForCurrentPhotoStage1.append(oneline)
            
                if idx == len(tempAllLines) - 1:
                    #move to new log.txt to continue record
                    tempAllLines = []
                    self.lastTimeEndWriteLogLinesIdx = -1
                    self.startLogSearchingFileIdx += 1
                    break
        
        ### Stage 2 ###
        
        if isNeedEnterStage2:
            print("Enter stage 2!")
            isNotReadyToLogNextPhoto = True
            stage2TempAllLines = []
            self.savedLogForCurrentPhotoStage2 = []
            while(isNotReadyToLogNextPhoto):
                if self.startLogSearchingFileIdx >= len(self.allUpdatedLogsFileName):
                    print("Search at the end of the last log, possibily due to loss log for this photo. Press Enter to continue...")
                    self.isParseError = True
                    self.parseErrorMessage = "照片: " + photoName + " 未找到對應的log片段，可能有掉log的問題存在。"
                    #log index out of bounds
                    break
                with open(self.inputLogPath + self.allUpdatedLogsFileName[self.startLogSearchingFileIdx], 'r', encoding="utf-8") as f:
                    lines = f.readlines()
                    f.close()
                    for line in lines:
                        stage2TempAllLines.append(line)
                for idx, oneline in enumerate(stage2TempAllLines):
                    if self.lastTimeEndWriteLogLinesIdx >= idx or oneline.startswith("-"):
                        continue
                    
                    oneline_split_hour = int(oneline.split(" ")[1].split(":")[0])
                    oneline_split_minute = int(oneline.split(" ")[1].split(":")[1])
                    oneline_split_second = int(oneline.split(" ")[1].split(":")[2].split(".")[0])
                    
                    if isFindFirstLine and self.containKeywords(oneline, saveKeyword):
                        #the current line is the end of recording because it shows to save the photo
                        self.savedLogForCurrentPhotoStage2.append(oneline)
                        isNotReadyToLogNextPhoto = False
                        self.lastTimeEndWriteLogLinesIdx = idx
                        break
                    elif (oneline_split_hour == after3secPhotoHour) and (oneline_split_minute == after3secPhotoMinute) and (oneline_split_second == after3secPhotoSecond):
                        #超過拍照3秒以後的時間，都沒有找到存檔的關鍵字log
                        print("WARNING: Loss log detected. Save keyword for photo %s is not found, log will stop record according to photo timestamp. Press Enter to continue..." % photoName)
                        stage2NotFoundSavePhotoLogPosition = True
                        isNotReadyToLogNextPhoto = False
                        #reset 3秒前的檔案跟index行數
                        self.startLogSearchingFileIdx = self.stage1captureTimestampFileIdx
                        self.lastTimeEndWriteLogLinesIdx = self.stage1captureTimestampLogLinesIdx
                        
                        break
                        
                    else:
                        if self.containKeywords(oneline, logRecordKeyword) and isFindFirstLine:
                            #append oneline to output log
                            self.savedLogForCurrentPhotoStage2.append(oneline)
                        
                        if idx == len(tempAllLines) - 1:
                            #move to new log.txt to continue record
                            stage2TempAllLines = []
                            self.lastTimeEndWriteLogLinesIdx = -1
                            self.startLogSearchingFileIdx += 1
                            break
        
        if self.exportEmptyLog:
            errorMessage = "The log information of photo %s is not fully recorded in the log file or loss log. Export empty log file." % photoName
            self.writeLogContent(self.outputPath, photoName, [errorMessage])
        elif stage2NotFoundSavePhotoLogPosition:
            #只寫入stage1留下來的log
            self.writeLogContent(self.outputPath, photoName, self.savedLogForCurrentPhotoStage1)
        else:
            #寫入stage1與stage2的log
            logsCombine = self.savedLogForCurrentPhotoStage1 + self.savedLogForCurrentPhotoStage2
            self.writeLogContent(self.outputPath, photoName, logsCombine)
        self.copyPhotoToOutputFolder(self.inputPhotoPath, photoName, self.outputPath)
    
    
    def getAfter3secTimestamp(self, currentPhotoTimestamp, timestampNamingRule):
        '''
        strptime naming rule can refer to https://www.geeksforgeeks.org/python-datetime-strptime-function/
        '''
        datetimeObject = datetime.datetime.strptime(currentPhotoTimestamp, timestampNamingRule)
        after3secDatetime = datetimeObject + datetime.timedelta(seconds=4)
        
        return after3secDatetime.hour, after3secDatetime.minute, after3secDatetime.second
    
    def getPreviousNSecTimestamp(self, currentPhotoTimestamp, timestampNamingRule, second=3):
        '''
        strptime naming rule can refer to https://www.geeksforgeeks.org/python-datetime-strptime-function/
        '''
        datetimeObject = datetime.datetime.strptime(currentPhotoTimestamp, timestampNamingRule)
        previous3secDatetime = datetimeObject - datetime.timedelta(seconds=second)
        
        return previous3secDatetime.hour, previous3secDatetime.minute, previous3secDatetime.second
    
    def getCurrentPhotoTimestamp(self, currentPhotoTimestamp, timestampNamingRule):
        '''
        strptime naming rule can refer to https://www.geeksforgeeks.org/python-datetime-strptime-function/
        '''
        datetimeObject = datetime.datetime.strptime(currentPhotoTimestamp, timestampNamingRule)
        
        return datetimeObject.hour, datetimeObject.minute, datetimeObject.second
    
    
    def parsePhotoExifTimestamp(self, inputPhotoPath, photoName):
        
        image = Image.open(inputPhotoPath + photoName)
        
        exif = image.getexif()
        for key, value in exif.items():
            if key in TAGS and TAGS[key] == "DateTime":
                return value
        
    
    def processPhoto(self, inputPhotoPath, photoName, isFirstPhoto, configSettings):
        global currentPhotoHour, currentPhotoMinute, currentPhotoSecond
    
        currentPhotoTimestamp = self.parsePhotoExifTimestamp(inputPhotoPath, photoName)
        
        #照片EXIF沒有記錄到時間，直接寫入錯誤訊息與輸出照片並回傳
        if currentPhotoTimestamp is None:
            errorMessage = "This photo EXIF does not contain time info."
            self.writeLogContent(self.outputPath, photoName, [errorMessage])
            self.copyPhotoToOutputFolder(self.inputPhotoPath, photoName, self.outputPath)
            return
        
        exifDateTimeFormat = "%Y:%m:%d %H:%M:%S"
        currentPhotoHour, currentPhotoMinute, currentPhotoSecond = self.getCurrentPhotoTimestamp(currentPhotoTimestamp, exifDateTimeFormat)
        #print("curHour: ", currentPhotoHour, "curMinute: ", currentPhotoMinute, "curSecond: ", currentPhotoSecond)
        
        prevNsecHour, prevNsecMinute, prevNsecSecond = self.getPreviousNSecTimestamp(currentPhotoTimestamp, exifDateTimeFormat, configSettings["previous_second_to_start_log"])
        #print("prevNsecHour: ", prevNsecHour, "prevNsecMinute: ", prevNsecMinute, "prevNsecSecond: ", prevNsecSecond)
        
        after3secPhotoHour, after3secPhotoMinute, after3secPhotoSecond = self.getAfter3secTimestamp(currentPhotoTimestamp, exifDateTimeFormat)
        #print("after3secPhotoHour: ", after3secPhotoHour, "after3secPhotoMinute: ", after3secPhotoMinute, "after3secPhotoSecond: ", after3secPhotoSecond)
        
        self.fetchLogContent(photoName, isFirstPhoto, prevNsecHour, prevNsecMinute, prevNsecSecond, after3secPhotoHour, after3secPhotoMinute, after3secPhotoSecond, configSettings["log_keyword"], configSettings["save_keyword"])
    
    
    def readConfigFile(self, configFolder, projectName):
        with open(configFolder + projectName + ".json") as jsonFile:
            return json.load(jsonFile)
    
    


if __name__ == "__main__":
    
    parser = UIParser("0_input_log\\", "0_input_photo\\", "1_output\\", "config\\", "SX3")
    
    parser.executeUIParser()
    