import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

from time import sleep
from subprocess import check_output, call

import threading


class Capture(QWidget):
    capture_fail_signal = pyqtSignal()
    log_info_signal = pyqtSignal(str)
    run_cmd_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.CAMERA_DEBUG = False
        self.state = threading.Condition()
        self.logger = None
        self.setting = None

    def capture(self, path = "", focus_time = 5, save_time = 1, capture_num = 1):

        rc = self.open_camera()
        if rc!=0: return False
        #wait for auto focus
        self.log_info_signal.emit('wait for auto focus')
        for i in range(focus_time):
            self.log_info_signal.emit(str(i))
            sleep(1)

        # capture
        for i in range(capture_num):
            self.press_camera_button()
            sleep(0.03) 
        sleep(save_time) #wait for save photo
        if self.setting["platform"] == "c6project": sleep(2)
        self.transfer_img(path, capture_num)
        if self.setting["platform"] == "c6project": sleep(1)
        return True

    def open_camera(self):
        if self.CAMERA_DEBUG: self.log_info_signal.emit('\nopen_camera')
        rc, r = self.logger.run_cmd("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA --ez com.google.assistant.extra.CAMERA_OPEN_ONLY true --ez android.intent.extra.CAMERA_OPEN_ONLY true --ez isVoiceQuery true --ez NoUiQuery true --es android.intent.extra.REFERRER_NAME android-app://com.google.android.googlequicksearchbox/https/www.google.com")
        return rc

    def clear_camera_folder(self):
        #delete from phone: adb shell rm self.CAMERA_PATH/*
        if self.CAMERA_DEBUG: self.log_info_signal.emit('\nclear_camera_folder')
        ######## 注意不要誤刪到系統!!!!! ########
        if self.setting["platform"] == "c7project":
            rc, r = self.logger.run_cmd("adb shell rm -rf /sdcard/DCIM/Camera/*") # 要回傳資料，所以不能用signal
        elif self.setting["platform"] == "c6project":
            rc, r = self.logger.run_cmd("adb shell rm -rf /sdcard/DCIM/Camera/*") # 要回傳資料，所以不能用signal
        
    def press_camera_button(self):
        #condition 1 screen on 2 camera open: adb shell input keyevent = CAMERA
        if self.CAMERA_DEBUG: self.log_info_signal.emit('\npress_camera_button')
        if self.setting["platform"] == "c7project":
            rc, r = self.logger.run_cmd("adb shell input keyevent = CAMERA")
        elif self.setting["platform"] == "c6project":
            rc, r = self.logger.run_cmd("adb shell input keyevent = KEYCODE_VOLUME_UP")
        

    def transfer_img(self, path='', capture_num = 1):
        if self.CAMERA_DEBUG: self.log_info_signal.emit("\ntransfer_img")
        # list all file
        rc, r = self.logger.run_cmd("adb shell ls -lt {}".format("/sdcard/DCIM/Camera/"))
        if rc!=0: return

        # find the last num
        file_names = r.split('\n')[1:capture_num+1] 
        file_names = [f.split(' ')[-1].replace('\r', '') for f in file_names]
        if self.CAMERA_DEBUG: self.log_info_signal.emit('file_names')
        if self.CAMERA_DEBUG: self.log_info_signal.emit("{}".format(file_names))
        if len(file_names)==0 or file_names[0] == '':
            self.capture_fail()
            self.log_info_signal.emit('正在重新拍攝...')
            self.capture(path=path, capture_num=capture_num)

        else:
            for i in range(capture_num):
                file_name = "/sdcard/DCIM/Camera/{}".format(file_names[i])
                if capture_num==1:
                    p = str(path+".jpg")
                else:
                    p = str(path+"_"+str(i)+".jpg")
                self.log_info_signal.emit('transfer {} to {}'.format(file_name, p))
                self.logger.run_cmd("adb pull {} {}".format(file_name, p))

    def capture_fail(self):
        self.capture_fail_signal.emit()
        self.state.acquire()
        self.state.wait()
        self.state.release()
