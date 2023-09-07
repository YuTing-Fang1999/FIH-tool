from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtCore
from PyQt5.QtGui import QCursor

def set_btn_enable(btn: QPushButton, enable):
    if enable:
        style =  "QPushButton {font-weight:bold; font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0); color:black;}"
        btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    else:
        style =  "QPushButton {font-weight:bold; font-size:12pt; font-family:微軟正黑體; background: rgb(150, 150, 150); color: rgb(100, 100, 100);}"
    btn.setStyleSheet(style)
    btn.setEnabled(enable)