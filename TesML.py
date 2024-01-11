import sys
from PyQt5.QtWidgets import QApplication
# import qdarktheme

# from NTU.ML.MLISPSimulator.MLGenDataset.MyWidget import MyWidget
# from NTU.ML.MLISPSimulator.MLPushParam.MyWidget import MyWidget
from NTU.ML.MLISPSimulator.SelectROI.MyWidget import MyWidget
# from NTU.perceptual_distance.controller import MainWindow_controller as MyWidget
# from NTU.ML.MLAlignDataset.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
# qdarktheme.setup_theme()
sys.exit(app.exec_())
