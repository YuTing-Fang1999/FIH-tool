from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QSizePolicy,QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QApplication, QTableWidget, QHeaderView, QLineEdit,
    QFileDialog, QScrollArea
)    
import cv2
import numpy as np
from TraditionalParamTuning.myPackage.set_btn_enable import set_btn_enable

import sys
sys.path.append(".")

from .ImageViewer import ImageViewer
from .ROI_Select_Window import ROI_Select_Window
from .Target_Select_Window import Target_Select_Window
from .MeasureWindow import MeasureWindow
import os
import random

class MyLineEdit(QLineEdit):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumWidth(50)
        self.setMaximumWidth(200)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

class DeleteBtn(QPushButton):
    def __init__(self, table, page):
        super().__init__()
        self.setCursor(Qt.PointingHandCursor)
        self.table = table
        self.page = page
        self.setText("刪除")
        self.clicked.connect(self.deleteClicked)
        self.setStyleSheet("QPushButton {font-weight:bold; font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0); color:black;}")

    def deleteClicked(self):
        button = self.sender()
        if button:
            row = self.table.indexAt(button.pos()).row()
            self.table.removeRow(row)
            # print("del row", row)
            self.page.target_rois.pop(row)
            self.page.my_rois.pop(row)
            self.page.draw_ROI(self.page.my_rois)

class ROI_Page(QWidget):
    alert_info_signal = pyqtSignal(str, str)
    capture_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.target_filepath = "./"
        self.filefolder="./"
        self.target_rois = []
        self.my_rois = []

        self.setup_UI()
        self.setup_controller()

    def setup_UI(self):

        # Widgets
        self.label_img = ImageViewer()
        self.label_img.setAlignment(Qt.AlignCenter)
        # self.label_img.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.ROI_select_window = ROI_Select_Window()
        self.target_select_window = Target_Select_Window()
        self.measure_window = MeasureWindow()

        self.table = QTableWidget()
        self.headers = ["type", "min", "max", "weight", "刪除紐"]
        self.table.setColumnCount(len(self.headers))   ##设置列数
        self.table.setHorizontalHeaderLabels(self.headers)

        self.btn_capture = QPushButton()
        self.btn_capture.setCursor(Qt.PointingHandCursor)
        self.btn_capture.setText("拍攝照片")
        self.btn_capture.setToolTip("會拍攝一張照片，請耐心等候")

        self.btn_gen_ref = QPushButton()
        self.btn_gen_ref.setCursor(Qt.PointingHandCursor)
        self.btn_gen_ref.setText("產生參考照片")
        self.btn_gen_ref.setToolTip("使用十張連拍做多幀降造產生參考照片")

        self.btn_load_target_pic = QPushButton("Load 參考照片")
        self.btn_load_target_pic.setCursor(Qt.PointingHandCursor)
        self.btn_load_target_pic.setToolTip("選擇參考照片")

        self.btn_add_ROI_item = QPushButton()
        self.btn_add_ROI_item.setCursor(Qt.PointingHandCursor)
        self.btn_add_ROI_item.setText("增加ROI區域")
        self.btn_add_ROI_item.setToolTip("按下後會新增一個目標區域")
        
        self.btn_add_target_item = QPushButton()
        self.btn_add_target_item.setCursor(Qt.PointingHandCursor)
        self.btn_add_target_item.setText("增加目標指標")
        self.btn_add_target_item.setToolTip("按下後會新增一個目標指標")
        self.btn_add_target_item.hide()

        self.GLayout = QGridLayout()

        # Arrange layout
        HLayout = QHBoxLayout()

        VBlayout = QVBoxLayout()
        VBlayout.addWidget(self.label_img)
        VBlayout.addWidget(self.btn_capture)
        VBlayout.addWidget(self.btn_gen_ref)
        VBlayout.addWidget(self.btn_load_target_pic)
        VBlayout.addWidget(self.btn_add_ROI_item)
        VBlayout.addWidget(self.btn_add_target_item)
        HLayout.addLayout(VBlayout)

        VBlayout = QVBoxLayout()
        VBlayout.addWidget(self.table)
        HLayout.addLayout(VBlayout)

        # HLayout.setStretch(0,1)
        # HLayout.setStretch(1,1)

        #Scroll Area Properties
        scroll_wrapper = QHBoxLayout(self)
        layout_wrapper = QWidget()
        layout_wrapper.setLayout(HLayout)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True)
        scroll.setWidget(layout_wrapper)
        scroll_wrapper.addWidget(scroll)

    def setup_controller(self):
        self.ROI_select_window.to_main_window_signal.connect(self.select_ROI)
        self.measure_window.to_main_window_signal.connect(self.set_target_score)
        self.target_select_window.to_main_window_signal.connect(self.set_target_score)

        self.btn_add_ROI_item.clicked.connect(self.add_ROI_item)
        self.btn_add_target_item.clicked.connect(self.add_target_item)
        self.btn_load_target_pic.clicked.connect(self.load_target_img)

        ##### capture #####
        self.btn_capture.clicked.connect(lambda: self.capture_signal.emit("capture"))
        self.btn_gen_ref.clicked.connect(lambda: self.capture_signal.emit("Ref_Pic/capture/capture"))
        
    # def select_ROI(self, my_x_y_w_h, my_roi_img, target_roi_img):
    #     self.measure_window.measure_target(my_x_y_w_h, my_roi_img, target_roi_img)

    def select_ROI(self, my_x_y_w_h, target_x_y_w_h, target_filepath):
        self.measure_window.measure_target(my_x_y_w_h, target_x_y_w_h, target_filepath)

    def set_target_score(self, my_x_y_w_h, target_x_y_w_h, target_type, target_score_min, target_score_max, target_filepath):
        
        for i in range(len(target_type)):
            self.add_to_table(target_type[i], target_score_min[i], target_score_max[i], 1)
            self.target_rois.append([target_filepath, target_x_y_w_h])
            self.my_rois.append(my_x_y_w_h)
            self.draw_ROI(self.my_rois)
        # # Auto resize the columns to fit their content
        # self.table.resizeColumnsToContents()

    def add_to_table(self, target_type, target_score_min, target_score_max, target_weight):

        row = self.table.rowCount()
        self.table.setRowCount(row + 1)

        label = QLabel(target_type)
        label.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row,0,label)

        self.table.setCellWidget(row,1,MyLineEdit(str(target_score_min)))

        self.table.setCellWidget(row,2,MyLineEdit(str(target_score_max)))

        self.table.setCellWidget(row,3,MyLineEdit(str(target_weight)))

        self.table.setCellWidget(row,4,DeleteBtn(self.table, self))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setStretchLastSection(True)
    
    def add_ROI_item(self):
        if len(self.ROI_select_window.my_viewer.img)==0:
            self.alert_info_signal.emit("未拍攝照片", "請先固定好拍攝位置，按拍攝鈕拍攝拍攝照片後，再選取區域")
            return
        
        if len(self.ROI_select_window.target_viewer.img)==0:
            self.alert_info_signal.emit("請先Load參考照片", "請先Load參考照片，再選取區域")
            return

        self.ROI_select_window.select_ROI()
        
    def add_target_item(self):
        self.target_select_window.select_target()

    def draw_ROI(self, rois):
        img_select = self.img.copy()
        # print('draw_ROI', rois)
        for i, roi in enumerate(rois):
            if len(roi)==0: continue

            x, y, w, h = roi
            # 隨機產生顏色
            color = [random.randint(0, 255), random.randint(0, 255),random.randint(0, 255)]
            cv2.rectangle(img_select, (x, y), (x+w, y+h), color, 10)
            cv2.putText(img_select, text=str(i+1), org=(x+w//2, y+h//2), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=min(w//50,h//50)+1, color=color, thickness=min(w//50,h//50)+1)

        self.label_img.setPhoto(img_select)

    def load_target_img(self):
        filepath, filetype = QFileDialog.getOpenFileName(
            self,
            "選擇target照片",
            self.filefolder,  # start path
            'Image Files(*.png *.jpg *.jpeg *.bmp)'
        )

        if filepath == '': return
        self.set_target_img(filepath)

    def set_target_img(self, filepath):
        self.filefolder = '/'.join(filepath.split('/')[:-1])
        self.filename = filepath.split('/')[-1]
        self.btn_load_target_pic.setText("Load 目標照片 ({})".format(self.filename))
        
        # load img
        img = cv2.imdecode(np.fromfile(file=filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
        self.ROI_select_window.target_label.setText(self.filename)
        self.ROI_select_window.target_viewer.set_img(img)
        self.ROI_select_window.filepath = filepath
        self.target_filepath = filepath
        
    def set_photo(self, img_name):
        img = cv2.imread(img_name)
        if img is None:
            self.alert_info_signal.emit("讀取照片失敗", "請確認照片路徑是否正確")
            return
        self.img = img
        self.label_img.setPhoto(img)
        self.ROI_select_window.my_label.setText(img_name)
        self.ROI_select_window.my_viewer.set_img(img)
        self.draw_ROI(self.my_rois)

    def set_all_enable_by_case(self, case):
        if case=="run":
            
            set_btn_enable(self.btn_capture, False)
            set_btn_enable(self.btn_gen_ref, False)
            set_btn_enable(self.btn_load_target_pic, False)
            set_btn_enable(self.btn_add_ROI_item, False)

            for row in range(self.table.rowCount()): 
                for col in range(self.table.columnCount()): 
                    _item = self.table.cellWidget(row, col) 
                    if _item:            
                        _item.setEnabled(False)
        
        elif case=="push" or case=="capture":
            set_btn_enable(self.btn_capture, False)
            set_btn_enable(self.btn_gen_ref, False)
            set_btn_enable(self.btn_load_target_pic, True)
            set_btn_enable(self.btn_add_ROI_item, True)

        elif case=="done":
            set_btn_enable(self.btn_capture, True)
            set_btn_enable(self.btn_gen_ref, True)
            set_btn_enable(self.btn_load_target_pic, True)
            set_btn_enable(self.btn_add_ROI_item, True)

            for row in range(self.table.rowCount()): 
                for col in range(self.table.columnCount()): 
                    _item = self.table.cellWidget(row, col) 
                    if _item:            
                        _item.setEnabled(True)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ROI_Page(None)
    window.showMaximized()
    sys.exit(app.exec_()) 