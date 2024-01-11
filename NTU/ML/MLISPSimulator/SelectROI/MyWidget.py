from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox, QFrame
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
from .ML_ROI_window import ROI_tune_window
import numpy as np
import cv2
import json

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__("NTU/ML/MLISPSimulator/SelectROI/") 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.select_ROI_window = ROI_tune_window()
        
        self.setupSettingUI()
        self.controller()
        
        
    def setupSettingUI(self):
        if self.get_path("img_path") != "./": 
            self.ui.img_path.setText(self.setting["img_path"])
        
    def controller(self):
        self.ui.load_img_btn.clicked.connect(lambda: self.load_img())
        self.ui.select_btn.clicked.connect(lambda: self.select())
        self.select_ROI_window.to_main_window_signal.connect(self.get_ROI_coordinate)
        
    def load_img(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.get_path("SelectROI_filefolder"),  # start path
                                                         'Image Files(*.png *.jpg *.jpeg *.bmp)')
        if filepath == "": return
        
        self.ui.img_path.setText(filepath)
        self.set_path("img_path", filepath)
        self.set_path("SelectROI_filefolder", '/'.join(filepath.split('/')[:-1]))
        
    def select(self):
        img = cv2.imdecode(np.fromfile(file=self.get_path("img_path"), dtype=np.uint8), cv2.IMREAD_COLOR)
        if(self.ui.ROI_text.toPlainText()!=""):
            ROI_arr = json.loads(self.ui.ROI_text.toPlainText())
        else:
            ROI_arr = []
        self.select_ROI_window.tune(-1, img, ROI_arr)
        
    def get_ROI_coordinate(self, idx, roi_coordinate):
        text = ""
        for roi in roi_coordinate:
            text += f"[{roi[0]}, {roi[1]}],"
        text = "[" + text[:-1] + "]"
        self.ui.ROI_text.setPlainText(text)
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())