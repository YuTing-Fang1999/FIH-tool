import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme

from NTU.ML.MLISPSimulator.MLGenDataset.MyWidget import MyWidget
# from NTU.ML.MLISPSimulator.MLPushParam.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())
