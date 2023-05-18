import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建一个QWidget对象作为窗口
    window = QWidget()
    
    # 使用setStyleSheet()方法设置背景色为红色
    window.setStyleSheet("background-color: red;")
    label = QPushButton(window)

    # 显示窗口
    window.show()

    sys.exit(app.exec_())
