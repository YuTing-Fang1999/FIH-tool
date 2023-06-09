from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QGuiApplication
from MainWindow import MainWindow
import qdarktheme

# if __name__ == '__main__':
#     # 高分辨率屏幕自適應
#     QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     # 設置支持小數放大比例（適應如125%的縮放比）  
#     QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)  
#     app = QApplication([])
#     # Apply the complete dark theme to your Qt App.
#     qdarktheme.setup_theme()
#     widget = MainWindow()
#     widget.showMaximized()
#     app.exec_()

##### MLGenDataset #####
import sys
from NTU.MLGenDataset.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
sys.exit(app.exec_())
    
##### TraditionalParamTuning #####
# from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5 import QtWidgets
# import sys
# from TraditionalParamTuning.controller import MainWindow_controller


# if __name__ == '__main__':
#     # 自適應分辨率
#     QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
#     # 設置支持小數放大比例（適應如125%的縮放比）  
#     QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)  

#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow_controller()
#     window.showMaximized()
#     sys.exit(app.exec_())