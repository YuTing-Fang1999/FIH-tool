import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme

# from NTU.ML.曲線逆推.lut_weight.MyWidget import MyWidget
from NTU.ML.曲線逆推.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())