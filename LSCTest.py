import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme
from QUL.LSC.MyWidget import MyWidget
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QGuiApplication

if __name__ == '__main__':
    # 高分辨率屏幕自適應
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # 設置支持小數放大比例（適應如125%的縮放比）  
    QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)  
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())