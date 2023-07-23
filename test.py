import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout

app = QApplication(sys.argv)

# 創建一個QWidget作為主窗口
window = QWidget()
window.setWindowTitle('QCheckBox 最大化示例')

# 創建一個QCheckBox
checkbox = QCheckBox('這是一個QCheckBox')

# 創建一個QVBoxLayout並將QCheckBox添加進去
layout = QVBoxLayout()
layout.addWidget(checkbox)

# 設置主窗口的佈局為剛剛創建的QVBoxLayout
window.setLayout(layout)

window.show()
sys.exit(app.exec_())
