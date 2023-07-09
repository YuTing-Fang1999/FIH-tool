from time import sleep
from .CMDRunner import CMDRunner
class Camera:

    def __init__(self, platform, cmd: CMDRunner):
        self.platform = platform
        self.cmd = cmd

        self.CAMERA_DEBUG = False
        self.pre_name_cache = []

    def capture(self, path = "", focus_time = 5, save_time = 2, transfer_time = 2, capture_num = 1):

        rc = self.open_camera()
        if rc!=0: return False
        #wait for auto focus
        print('wait for auto focus')
        for i in range(focus_time):
            print(str(i))
            sleep(1)

        # capture
        for i in range(capture_num):
            self.press_camera_button()
            sleep(0.03) 
        sleep(save_time) #wait for save photo
        
        if self.platform == "c6project": sleep(2)
        self.back_to_home()
        self.transfer_img(path, capture_num)
        if self.platform == "c6project": sleep(1)
        sleep(transfer_time)
        return True

    def open_camera(self):
        if self.CAMERA_DEBUG: print('\nopen_camera')
        rc, r = self.cmd.run("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA --ez com.google.assistant.extra.CAMERA_OPEN_ONLY true --ez android.intent.extra.CAMERA_OPEN_ONLY true --ez isVoiceQuery true --ez NoUiQuery true --es android.intent.extra.REFERRER_NAME android-app://com.google.android.googlequicksearchbox/https/www.google.com")
        return rc

    def clear_camera_folder(self):
        self.back_to_home()
        #delete from phone: adb shell rm self.CAMERA_PATH/*
        if self.CAMERA_DEBUG: print('\nclear_camera_folder')
        ######## 注意不要誤刪到系統!!!!! ########
        if self.platform == "c7project":
            rc, r = self.cmd.run("adb shell rm -rf /sdcard/DCIM/Camera/*") # 要回傳資料，所以不能用signal
        elif self.platform == "c6project":
            rc, r = self.cmd.run("adb shell rm -rf /sdcard/DCIM/Camera/*") # 要回傳資料，所以不能用signal
            
        self.pre_name_cache = []
        
    def press_camera_button(self):
        #condition 1 screen on 2 camera open: adb shell input keyevent = CAMERA
        if self.CAMERA_DEBUG: print('\npress_camera_button')
        if self.platform == "c7project":
            rc, r = self.cmd.run("adb shell input keyevent = CAMERA")
        elif self.platform == "c6project":
            rc, r = self.cmd.run("adb shell input keyevent = KEYCODE_VOLUME_UP")
        

    def transfer_img(self, path='', capture_num = 1):
        
        if self.CAMERA_DEBUG: print("\ntransfer_img")
        # list all file
        rc, r = self.cmd.run("adb shell ls -lt {}".format("/sdcard/DCIM/Camera/"))
        if rc!=0: return

        # find the last num
        file_names = r.split('\n')[1:capture_num+1] 
        file_names = [f.split(' ')[-1].replace('\r', '') for f in file_names]
        if self.CAMERA_DEBUG: print('file_names')
        if self.CAMERA_DEBUG: print("{}".format(file_names))
        if len(file_names)==0 or file_names[0] == '':
            input('確認好相機後按enter')
            print('正在重新拍攝...')
            self.capture(path=path, capture_num=capture_num)

        else:
            for i in range(capture_num):
                file_name = "/sdcard/DCIM/Camera/{}".format(file_names[i])
                if capture_num==1:
                    p = str(path+".jpg")
                else:
                    p = str(path+"_"+str(i)+".jpg")
                    
                if file_name in self.pre_name_cache: 
                    print('************ERROR**************\n 存到之前的照片了')
                    input('確認好後按enter')
                if self.CAMERA_DEBUG: print('transfer {} to {}'.format(file_name, p))
                self.cmd.run("adb pull {} {}".format(file_name, p))
                self.pre_name_cache.append(file_name) 
                
    def back_to_home(self):
        self.cmd.run("adb shell input keyevent BACK")

if __name__ == "__main__":
    from CMDRunner import CMDRunner
    cmd = CMDRunner()
    camera = Camera("c7project", cmd)
    camera.capture(path="test")
    # param_list = []
    # # 開啟 CSV 檔案
    # with open('param_denorm.csv', newline='') as csvfile:

    #     # 讀取 CSV 檔案內容
    #     rows = csv.reader(csvfile)
    #     param_list = list(rows)

    # # 以迴圈輸出每一列
    # for param in tqdm(range(len(param_list))):
    #     sleep(0.01)