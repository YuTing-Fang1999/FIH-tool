from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget
import json

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__() 
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.controller()
        
    def controller(self):
        self.ui.load_config_btn.clicked.connect(lambda: self.set_load_config())
    
    def set_load_config(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         self.get_filefolder("ML_config_filefolder"),  # start path
                                                         '*.json')

        if filepath == '':
            return
        
        filefolder = '/'.join(filepath.split('/')[:-1])
        self.set_filefolder("ML_config_filefolder", filefolder)
        
        config = self.read_json(filepath)
        self.ui.config_path.setText(filepath)
        
        self.ui.platform.setText(config["platform"])
        self.ui.project_path.setText(config["project_path"])
        self.ui.trigger_idx.setText(str(config["trigger_idx"]))
        self.ui.gen_num.setText(str(config["gen_num"]))
        self.ui.step.setText(str(config["step"]))
        # self.ui.param_name.setText(config["param_name"])
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())