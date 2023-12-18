from PyQt5.QtWidgets import (
    QTabWidget, QStatusBar, QWidget, QLabel,
    QMainWindow, QMessageBox, QToolButton,
    QVBoxLayout, QScrollArea, QSplitter,
    QFileDialog, QInputDialog, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from TraditionalParamTuning.myPackage.Capture import Capture
from TraditionalParamTuning.myPackage.Tuning import Tuning
from TraditionalParamTuning.myPackage.get_file_path import get_file_path_c7, get_file_path_c6
from TraditionalParamTuning.myPackage.read_param_value import read_param_value_c7, read_param_value_c6
from TraditionalParamTuning.myPackage.read_trigger_data import read_trigger_data_c7, read_trigger_data_c6
from TraditionalParamTuning.myPackage.set_param_value import set_param_value_c7, set_param_value_c6
from TraditionalParamTuning.myPackage.build_and_push import build_and_push_c7, build_and_push_c6

from TraditionalParamTuning.myPackage.Ref_Pic import gen_ref_denoise, gen_ref_sharpness

import os
import xml.etree.ElementTree as ET
import json
import threading
import ctypes, inspect
from time import sleep
import shutil

from TraditionalParamTuning.UI.MainWindow import MainWindow

class MainWindow_controller(QWidget):
    set_ROI_page_photo_signal = pyqtSignal()

    def __init__(self):
        super().__init__() 
        self.origin_dir = os.getcwd()
        self.get_file_path = {}
        self.get_file_path["c6project"] = get_file_path_c6
        self.get_file_path["c7project"] = get_file_path_c7

        self.read_param_value = {}
        self.read_param_value["c6project"] = read_param_value_c6
        self.read_param_value["c7project"] = read_param_value_c7

        self.read_trigger_data = {}
        self.read_trigger_data["c6project"] = read_trigger_data_c6
        self.read_trigger_data["c7project"] = read_trigger_data_c7

        self.set_param_value = {}
        self.set_param_value["c6project"] = set_param_value_c6
        self.set_param_value["c7project"] = set_param_value_c7

        self.build_and_push = {}
        self.build_and_push["c6project"] = build_and_push_c6
        self.build_and_push["c7project"] = build_and_push_c7

        self.capture = Capture()
        self.setting = self.read_setting()
        self.config = self.read_config()
        
        self.ui = MainWindow()
        self.ui.setup_UI(self)
        self.set_UI_data(self.setting)

        self.capture.logger = self.ui.logger
        self.capture.setting = self.setting
        self.tuning = Tuning( self.ui.logger, self.ui.run_page.lower_part, 
                                self.setting, self.config, self.capture, 
                                self.set_param_value, self.build_and_push, self.get_file_path)

        self.setup_controller()
        self.set_all_enable_by_case("done")

    def setup_controller(self):
        self.ui.tabWidget.setTabEnabled(1, True)
        ########## trigger ##########
        #############################

        ##### project_page #####
        self.ui.project_page.platform_selector.buttongroup1.buttonClicked.connect(self.onPlatformSelecterClicked)
        self.ui.project_page.btn_select_project.clicked.connect(self.select_project)
        self.ui.project_page.btn_select_exe.clicked.connect(self.select_exe)

        ##### param page #####
        self.ui.param_page.trigger_selector.currentIndexChanged[int].connect(self.set_trigger_idx)
        self.ui.param_page.ISP_tree.tree.itemClicked.connect(self.ISP_tree_itemClicked)
        self.ui.param_page.push_and_save_block.btn_input_param.clicked.connect(self.input_param)

        ##### run page #####
        self.ui.run_page.upper_part.btn_run.clicked.connect(self.run)
        self.ui.run_page.upper_part.btn_param_window.clicked.connect(self.show_param_window)

        ########## trigger ##########
        #############################

        ########## tuning ###########
        #############################

        # tuning to param window
        self.tuning.update_param_window_scores_signal.connect(self.ui.param_window.update_scores)
        self.tuning.update_param_window_signal.connect(self.ui.param_window.update)
        self.tuning.setup_param_window_signal.connect(self.ui.param_window.setup)

        # tuning to UI
        self.tuning.finish_signal.connect(self.finish)
        self.tuning.set_score_signal.connect(self.ui.run_page.upper_part.set_score)
        self.tuning.set_generation_signal.connect(self.ui.run_page.upper_part.set_generation)
        self.tuning.set_individual_signal.connect(self.ui.run_page.upper_part.set_individual)

        # tuning logger
        self.tuning.log_info_signal.connect(self.ui.logger.show_info)
        self.tuning.run_cmd_signal.connect(self.ui.logger.run_cmd)

        ########## tuning ###########
        #############################

        ##### capture signal #####
        self.capture.capture_fail_signal.connect(self.capture_fail)
        self.capture.log_info_signal.connect(self.ui.logger.show_info)
        self.capture.run_cmd_signal.connect(self.ui.logger.run_cmd)

        # alert_info_signal
        self.ui.project_page.alert_info_signal.connect(self.alert_info)
        self.ui.ROI_page.alert_info_signal.connect(self.alert_info)
        self.ui.param_page.push_and_save_block.alert_info_signal.connect(self.alert_info)
        self.ui.run_page.upper_part.alert_info_signal.connect(self.alert_info)
        self.tuning.alert_info_signal.connect(self.alert_info)

        # do_capture
        self.ui.ROI_page.capture_signal.connect(self.do_capture_start)
        self.ui.param_page.push_and_save_block.capture_signal.connect(self.do_capture_start)
        self.set_ROI_page_photo_signal.connect(lambda: self.ui.ROI_page.set_photo("capture.jpg"))

        self.ui.param_page.push_and_save_block.get_and_set_param_value_signal.connect(self.get_and_set_param_value_slot)
        self.ui.param_page.push_and_save_block.push_to_camera_signal.connect(self.get_and_build_and_push_start)
    
    def input_param(self):
        try:
            text, okPressed = QInputDialog.getMultiLineText(self, "參數輸入","直接複製csv的參數即可\nex:[0.06 0.37 0.18 0.5  0.2  0.06 0.2  0.05]", "")
            if okPressed and text != '':
                text = text.replace('[','')
                text = text.replace(']','')
                text = text.split()
                param_value = [ float(t) for t in text ]
                self.ui.logger.show_info("input_param: {}".format(param_value))
                self.ui.param_page.param_modify_block.update_param_value(param_value)
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
        

    def get_and_set_param_value_slot(self):
        try:
            key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
            param_value = self.ui.param_page.param_modify_block.get_param_value()
            self.setting["trigger_idx"] = self.ui.param_page.trigger_selector.currentIndex()
            self.ui.logger.show_info('write {} to {}/{}, trigger_idx: {}'.format(param_value, self.setting["root"] ,self.setting["key"], self.setting["trigger_idx"]))
            file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], key_config["file_path"])
            self.set_param_value[self.setting["platform"]](self.setting["key"], key_config, file_path, self.setting["trigger_idx"], param_value)
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
        
    def get_and_build_and_push_start(self, is_capture, saved_path):
        self.setting["bin_name"] = self.ui.project_page.lineEdits_bin_name.text()
        # 建立一個子執行緒
        self.push_task = threading.Thread(target=lambda: self.build_and_push_logger(self.setting["exe_path"], self.setting["project_path"], self.setting["bin_name"], is_capture, saved_path))
        # 當主程序退出，該執行緒也會跟著結束
        self.push_task.daemon = True
        # 執行該子執行緒
        self.push_task.start()

    def build_and_push_logger(self, exe_path, project_path, bin_name, is_capture, saved_path):
        try:
            self.set_all_enable_by_case("push")
            self.ui.logger.show_info('push bin to camera...')
            self.ui.logger.run_cmd('adb shell input keyevent = KEYCODE_HOME')
            self.build_and_push[self.setting["platform"]](self.ui.logger, exe_path, project_path, bin_name)
            self.capture.clear_camera_folder()
            self.ui.logger.show_info('wait for reboot camera...')
            sleep(7)
            if is_capture: self.do_capture(saved_path)
            else:
                self.set_all_enable_by_case("done")
                self.ui.logger.show_info("done")
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
        

    def do_capture_start(self, saved_path):
        self.capture_task = threading.Thread(target=lambda: self.do_capture(saved_path))
        self.capture_task.daemon = True
        self.capture_task.start()

    def do_capture(self, saved_path):
        try:
            self.set_all_enable_by_case("capture")

            if(saved_path=="Ref_Pic/capture/capture"):
                if os.path.exists('Ref_Pic'): shutil.rmtree('Ref_Pic')
                self.tuning.mkdir("Ref_Pic")
                self.tuning.mkdir("Ref_Pic/capture")
                N=10
                if self.capture.capture(saved_path, capture_num=N):
                    gen_ref_denoise(N)
                    gen_ref_sharpness(N)

            elif (saved_path=="capture"):
                if self.capture.capture(saved_path, capture_num=1):
                    self.set_ROI_page_photo_signal.emit()

            else:
                self.capture.capture(saved_path, capture_num=1)

            self.set_all_enable_by_case("done")
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
        
        
    def set_platform_UI(self):
        try:
            if self.ui.project_page.platform_selector.buttongroup1.checkedId() == 1:
                self.setting["platform"] = self.ui.project_page.platform_selector.rb1.text()
                self.ui.project_page.setc6Form()

            if self.ui.project_page.platform_selector.buttongroup1.checkedId() == 2:
                self.setting["platform"] = self.ui.project_page.platform_selector.rb2.text()
                self.ui.project_page.setc7Form()
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def onPlatformSelecterClicked(self):
        try:
            self.ui.param_page.reset_UI()
            self.ui.project_page.label_project_path.setText("")
            self.ui.project_page.label_exe_path.setText("")
            self.ui.tabWidget.setTabEnabled(1, False)
            self.ui.tabWidget.setTabEnabled(2, False)
            self.ui.tabWidget.setTabEnabled(3, False)
            self.set_platform_UI()
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
        
    def ISP_tree_itemClicked(self, item, col):
        try:
            if item.parent() is None: 
                if item.isExpanded():item.setExpanded(False)
                else: item.setExpanded(True)
                return

            root = item.parent().text(0)
            key = item.text(0)
            self.change_page_to(root, key)
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def change_page_to(self, root, key):
        try:
            self.setting["root"] = root
            self.setting["key"] = key
            if self.ui.param_page.trigger_selector.currentIndex() != -1:
                self.setting["trigger_idx"] = self.ui.param_page.trigger_selector.currentIndex()
            self.ui.logger.signal.emit('Change param page to {}/{}'.format(root, key))

            key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
            key_data = self.setting[self.setting["root"]][self.setting["key"]]

            ##### param_page UI #####
            self.ui.param_page.param_modify_block.update_UI(key_config)
            self.ui.param_page.param_range_block.update_UI(key_config)
            self.ui.param_page.param_range_block.update_defult_range(key_config["defult_range"])
            if "coustom_range" in key_data and len(key_data["coustom_range"])>0:
                self.ui.param_page.param_range_block.update_coustom_range(key_data["coustom_range"])
            else:
                self.ui.param_page.param_range_block.update_coustom_range(key_config["defult_range"])

            #### trigger ####
            
            file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], key_config["file_path"])
            aec_trigger_datas = self.read_trigger_data[self.setting["platform"]](key_config, file_path)
            self.ui.param_page.trigger_selector.update_UI(aec_trigger_datas)
            
            self.ui.param_page.trigger_selector.setCurrentIndex(self.setting["trigger_idx"])
            # self.set_trigger_idx(self.setting["trigger_idx"])
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def select_project(self):
        try:
            path = QFileDialog.getExistingDirectory(self,"選擇project", self.ui.project_page.defult_path) # start path
            if path == "": return
            self.ui.project_page.defult_path = '/'.join(path.split('/')[:-1])
            self.ui.project_page.label_project_path.setText(path)

            self.ui.logger.show_info('\nset_project')
            self.setting['project_name'] = path.split('/')[-1]
            self.setting['project_path'] = path
            self.set_project(path)
            self.get_UI_data()
            self.write_setting()
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def select_exe(self):
        try:
            path, filetype = QFileDialog.getOpenFileName(self,"選擇ParameterParser", self.ui.project_page.defult_path) # start path
            if path == "": return
            self.ui.project_page.defult_path = '/'.join(path.split('/')[:-1])
            self.ui.project_page.label_exe_path.setText(path)
            self.setting["exe_path"] = path
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def set_project(self, project_path):
        try:
            ##### ISP_Tree #####
            tree_data = {}
            for root in self.config[self.setting["platform"]]:
                self.setting["root"] = root
                self.setting[root] = {}
                tree_data[root] = []
                for key in self.config[self.setting["platform"]][root]:
                    self.setting["key"] = key
                    self.setting[root][key] = {}
                    tree_data[root].append(key)
            self.ui.param_page.ISP_tree.update_UI(tree_data)

            key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
            file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], key_config["file_path"])
            print(file_path)
            if not os.path.exists(file_path): 
                self.ui.logger.show_info("找不到"+file_path+"\n請確認"+self.setting["project_path"]+"是否為"+self.setting["platform"])
                self.ui.project_page.label_project_path.setText("找不到"+file_path+"\n請確認"+self.setting["project_path"]+"是否為"+self.setting["platform"])
                self.ui.param_page.reset_UI()
                return

            self.ui.logger.show_info("Load {} Successfully".format(self.setting["project_name"]))

            self.ui.tabWidget.setTabEnabled(1, True)
            self.ui.tabWidget.setTabEnabled(2, True)
            self.ui.tabWidget.setTabEnabled(3, True)

            self.change_page_to(self.setting["root"], self.setting["key"])
            self.set_trigger_idx(self.setting["trigger_idx"])
            
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def set_trigger_idx(self, trigger_idx):
        try:
            if trigger_idx==-1:
                self.ui.logger.signal.emit("set_trigger_idx return because trigger_idx=-1")
                return
            self.ui.logger.signal.emit('trigger_idx: {}'.format(trigger_idx))

            key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
            
            file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], key_config["file_path"])
            param_value = self.read_param_value[self.setting["platform"]](self.setting["key"], key_config, file_path, trigger_idx)
            self.ui.param_page.param_modify_block.update_param_value(param_value)
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def run(self):
        if self.tuning.is_run:
            self.finish(True)
        else:
            self.start()

    def start(self):
        if not self.get_UI_data(alert=True): return
        self.ui.logger.clear_info()
        self.ui.logger.signal.emit("START")
        self.set_all_enable_by_case("run")

        self.tuning.is_run = True
        self.ui.run_page.upper_part.btn_run.setText('STOP')
        self.ui.run_page.upper_part.mytimer.startTimer()
        
        # 建立一個子執行緒
        self.tuning_task = threading.Thread(target=lambda: self.tuning.run())
        # 當主程序退出，該執行緒也會跟著結束
        self.tuning_task.daemon = True
        # 執行該子執行緒
        self.tuning_task.start()

    def finish(self, success):
        self.ui.logger.signal.emit("STOP")
        self.tuning.is_run = False
        self.ui.run_page.upper_part.btn_run.setText('Run')
        self.ui.run_page.upper_part.mytimer.stopTimer()
        self.set_all_enable_by_case("done")
        # self.tuning.ML.save_model()
        os.chdir(self.origin_dir)
        if success: self.tuning.finish()
        stop_thread(self.tuning_task)

    def show_param_window(self):
        self.ui.param_window.close()
        self.ui.param_window.resize(400, 400)
        self.ui.param_window.showNormal()

    def capture_fail(self):
        if self.tuning.is_run: self.ui.run_page.upper_part.mytimer.stopTimer()
        QMessageBox.about(self, "拍攝未成功", "拍攝未成功\n請多按幾次拍照鍵測試\n再按ok鍵重新拍攝")
        self.capture.state.acquire()
        self.capture.state.notify()  # Unblock self if waiting.
        self.capture.state.release()
        if self.tuning.is_run: self.ui.run_page.upper_part.mytimer.continueTimer()
    
    def alert_info(self, title, text):
        # print(title)
        self.ui.logger.signal.emit(text)
        QMessageBox.about(self, title, text)

    def set_all_enable_by_case(self, case):
        self.ui.ROI_page.set_all_enable_by_case(case)
        if case=="run":
            self.ui.project_page.set_all_enable(False)
            self.ui.param_page.push_and_save_block.set_all_enable(False)
        
        elif case=="push" or case=="capture":
            self.ui.project_page.set_all_enable(False)
            # self.ui.ROI_page.set_btn_enable(False)
            self.ui.param_page.push_and_save_block.set_all_enable(False)
            self.ui.run_page.upper_part.btn_run.setEnabled(False)
            self.ui.run_page.upper_part.set_all_enable_by_case(case)

        elif case=="done":
            self.ui.project_page.set_all_enable(True)
            # self.ui.ROI_page.set_btn_enable(True)
            self.ui.param_page.push_and_save_block.set_all_enable(True)
            self.ui.run_page.upper_part.btn_run.setEnabled(True)
            self.ui.run_page.upper_part.set_all_enable_by_case(case)


    def set_UI_data(self, setting):
        try:
            if "trigger_idx" not in self.setting: self.setting["trigger_idx"] = 0
            
            ##### project_page #####
            if "platform" in setting:
                self.ui.project_page.platform_selector.set_platform(setting["platform"])
                self.set_platform_UI()

            if "project_path" in setting:
                self.ui.project_page.label_project_path.setText(setting["project_path"])

                if os.path.exists(setting["project_path"]):
                    self.set_project(setting["project_path"])

            if "exe_path" in setting:
                self.ui.project_page.label_exe_path.setText(setting["exe_path"])
            else:
                setting["exe_path"] = ""
            if "bin_name" in setting:
                self.ui.project_page.lineEdits_bin_name.setText(setting["bin_name"])
            else:
                setting["bin_name"] = ""

            ##### ROI_page #####
            if os.path.exists('capture.jpg'):
                self.ui.ROI_page.set_photo('capture.jpg')
                if "my_rois" in setting:
                    self.ui.ROI_page.target_rois = setting["target_rois"]
                    self.ui.ROI_page.my_rois = setting["my_rois"]
                    self.ui.ROI_page.draw_ROI(self.ui.ROI_page.my_rois)

            if 'target_type' in setting and len(setting["target_type"])>0:
                assert len(setting["my_rois"]) == len(setting["target_type"])
                for i in range(len(setting["target_type"])):
                    self.ui.ROI_page.add_to_table(setting["target_type"][i], setting["target_score_min"][i], setting["target_score_max"][i], setting["target_weight"][i])
            
            if "target_filepath" in self.setting and self.setting["target_filepath"] != "./":
                if os.path.exists(self.setting["target_filepath"]):
                    self.ui.ROI_page.target_filepath = self.setting["target_filepath"]
                    self.ui.ROI_page.set_target_img(self.setting["target_filepath"])

            ##### param_page #####
            if "root" in self.setting:
                key_data = self.setting[self.setting["root"]][self.setting["key"]]
                if "param_change_idx" in key_data: 
                    self.ui.param_page.param_modify_block.update_param_change_idx(key_data["param_change_idx"])

            for i, name in enumerate(self.ui.param_page.hyper_setting_block.hyper_param_name):
                if name in self.setting:
                    self.ui.param_page.hyper_setting_block.lineEdits_hyper_setting[i].setText(str(self.setting[name]))

            if 'saved_dir_name' in self.setting:
                self.ui.param_page.push_and_save_block.lineEdits_dir_name.setText(self.setting['saved_dir_name'])
            if 'saved_img_name' in self.setting:
                self.ui.param_page.push_and_save_block.lineEdits_img_name.setText(self.setting['saved_img_name'] )

            if "method" not in self.setting: self.setting['method'] = "global search"
            if self.setting['method'] == "local search":
                self.ui.param_page.hyper_setting_block.method_selector.setCurrentIndex(1)
            else:
                self.ui.param_page.hyper_setting_block.method_selector.setCurrentIndex(0)

            if "init_param" not in self.setting: self.setting['init_param'] = "使用目前gain的參數"
            if self.setting['init_param'] == "使用目前gain的參數":
                self.ui.param_page.hyper_setting_block.init_param_selector.setCurrentIndex(1)
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))
            
    def get_UI_data(self, alert=False):
        try:
            ##### project_page #####
            # 在選擇時已儲存到setting
                    # self.setting["project_path"]
                    # self.setting["exe_path"]
            self.setting["bin_name"] = self.ui.project_page.lineEdits_bin_name.text()

            ##### ROI_page #####
            self.setting["target_filepath"] = self.ui.ROI_page.target_filepath
            self.setting["target_rois"] = self.ui.ROI_page.target_rois
            self.setting["my_rois"] = self.ui.ROI_page.my_rois
            assert len(self.setting["my_rois"]) == self.ui.ROI_page.table.rowCount()

            self.setting["target_type"] = []
            self.setting["target_score_min"] = []
            self.setting["target_score_max"] = []
            self.setting["target_weight"] = []
            for i in range(self.ui.ROI_page.table.rowCount()):
                self.setting["target_type"].append(self.ui.ROI_page.table.cellWidget(i, 0).text())
                self.setting["target_score_min"].append(float(self.ui.ROI_page.table.cellWidget(i, 1).text()))
                self.setting["target_score_max"].append(float(self.ui.ROI_page.table.cellWidget(i, 2).text()))
                self.setting["target_weight"].append(float(self.ui.ROI_page.table.cellWidget(i, 3).text()))

            ##### param_page #####
            self.setting['method'] = self.ui.param_page.hyper_setting_block.method_selector.currentText()
            self.setting['init_param'] = self.ui.param_page.hyper_setting_block.init_param_selector.currentText()

            self.setting["trigger_idx"] = self.ui.param_page.trigger_selector.currentIndex()
            self.setting["trigger_name"] = self.ui.param_page.trigger_selector.currentText()

            if self.setting['method'] == "local search" and self.setting['init_param'] == "使用前一個gain的參數":
                if alert and self.setting["trigger_idx"]-1 < 0:
                    self.alert_info("「參數設定」頁面的初始化參數選項錯誤", "「參數設定」的local search方法設定錯誤\n第一個gain不能使用前一個gain的參數\n只能使用目前參數作為初始化參數")
                    return False

            if "root" in self.setting:
                key_data = self.setting[self.setting["root"]][self.setting["key"]]
                if self.setting['method'] == "local search" and self.setting['init_param'] == "使用前一個gain的參數":
                    key_config = self.config[self.setting["platform"]][self.setting["root"]][self.setting["key"]]
                    file_path = self.get_file_path[self.setting["platform"]](self.setting["project_path"], key_config["file_path"])
                    key_data["param_value"] = self.read_param_value[self.setting["platform"]](self.setting["key"], key_config, file_path, self.setting["trigger_idx"]-1)
                else:
                    key_data["param_value"] = self.ui.param_page.param_modify_block.get_param_value()
                
                key_data["param_change_idx"] = self.ui.param_page.param_modify_block.get_param_change_idx()

                key_data["coustom_range"] = []
                for item in self.ui.param_page.param_range_block.param_range_items:
                    for lineEdit in item.lineEdits_coustom_range:
                        if lineEdit.text() != "": 
                            key_data["coustom_range"].append(json.loads(lineEdit.text()))

            for i, name in enumerate(self.ui.param_page.hyper_setting_block.hyper_param_name):
                if self.ui.param_page.hyper_setting_block.lineEdits_hyper_setting[i].isVisibleTo(self.ui.param_page):
                    if self.ui.param_page.hyper_setting_block.lineEdits_hyper_setting[i].text()=="":
                        if alert:
                            self.alert_info("「參數設定」頁面的超參數的部分未填", "「參數設定」頁面「Hyper Parameters」的參數未填滿")
                            return False
                        else:
                            self.setting[name] = ""
                    else:
                        self.setting[name] = int(self.ui.param_page.hyper_setting_block.lineEdits_hyper_setting[i].text())
            if self.setting["population size"]<=4:
                self.alert_info("「參數設定」頁面的population size設定錯誤", "「參數設定」頁面的population size須設定大於4的數值")
            
            self.setting['saved_dir_name'] = self.ui.param_page.push_and_save_block.lineEdits_dir_name.text()
            self.setting['saved_img_name'] = self.ui.param_page.push_and_save_block.lineEdits_img_name.text()

            return True
        except Exception as error:
            print(error)
            self.alert_info("Failed", "Failed\n"+str(error))

    def read_setting(self):
        if os.path.exists('TraditionalParamTuning/setting.json'):
            with open('TraditionalParamTuning/setting.json', 'r') as f:
                return json.load(f)

        else:
            print("找不到設定檔，重新生成一個新的設定檔")
            return {
                "population size": 5,
                "generations": 20,
                "capture num": 1
            }

    def read_config(self):
        assert os.path.exists('TraditionalParamTuning/config')
        config = {}
        for name in os.listdir('TraditionalParamTuning/config'):
            with open('TraditionalParamTuning/config/'+name, 'r') as f:
                config[name.split('.')[0]] = json.load(f)

        return config

    def write_setting(self):
        print('TraditionalParamTuning/write_setting')
        with open("TraditionalParamTuning/setting.json", "w") as outfile:
            outfile.write(json.dumps(self.setting, indent=4))

    def closeEvent(self, event):
        if self.ui.param_window: self.ui.param_window.close()
        print('window close')
        self.get_UI_data()
        self.write_setting()


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