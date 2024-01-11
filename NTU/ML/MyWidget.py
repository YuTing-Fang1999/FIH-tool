from PyQt5.QtWidgets import QTabWidget, QApplication, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
# from .UI import Ui_Form
from myPackage.ParentWidget import ParentWidget

from NTU.ML.MLISPSimulator.MLGenDataset.MyWidget import MyWidget as MLGenDatasetWidget
from NTU.ML.MLISPSimulator.MLGenDataset.Intro import Intro as MLGenDatasetIntro
from NTU.ML.MLAlignDataset.MyWidget import MyWidget as MLAlignDatasetWidget
from NTU.ML.MLAlignDataset.Intro import Intro as MLAlignDatasetIntro
from NTU.ML.MLISPSimulator.SelectROI.MyWidget import MyWidget as MLSelectROIWidget
from NTU.ML.MLTrain.Intro import Intro as MLTrainIntro
from NTU.ML.MLRecommand.Intro import Intro as MLRecommandIntro
from NTU.ML.MLISPSimulator.MLPushParam.MyWidget import MyWidget as MLPushParamWidget

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()  # in python3, super(Class, self).xxx = super().xxx
        self.setupUi()
        self.controller()

    def setupUi(self):
        
        self.tabWidget = QTabWidget()

        self.gen_dataset_page = MLGenDatasetWidget()
        self.align_dataset_page = MLAlignDatasetWidget()
        self.select_ROI_page = MLSelectROIWidget()
        self.train_intro_page = MLTrainIntro()
        self.recommand_intro_page = MLRecommandIntro()
        self.push_param_page = MLPushParamWidget()

        self.tabWidget.addTab(self.gen_dataset_page, "GenDataset")
        self.tabWidget.addTab(self.align_dataset_page, "AlignDataset")
        self.tabWidget.addTab(self.select_ROI_page, "SelectROI")
        self.tabWidget.addTab(self.train_intro_page, "TrainIntro")
        self.tabWidget.addTab(self.recommand_intro_page, "RecommandIntro")
        self.tabWidget.addTab(self.push_param_page, "PushParam")
        
        wrapper = QVBoxLayout(self)
        wrapper.addWidget(self.tabWidget)
    def controller(self):
        pass
        
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = MyWidget()
    Form.show()
    sys.exit(app.exec_())