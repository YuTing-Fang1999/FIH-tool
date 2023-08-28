import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QGuiApplication

from NTU.ML.曲線逆推.MyWidget import MyWidget
# 高分辨率屏幕自適應
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# 設置支持小數放大比例（適應如125%的縮放比）  
QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough) 
 
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())