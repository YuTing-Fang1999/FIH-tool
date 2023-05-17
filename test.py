from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
import sys

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

# 创建一个 QListWidget
list_widget = QListWidget()

# 创建表头项
header_item = QListWidgetItem()
header_label = QLabel("表头")
header_label.setStyleSheet("font-weight: bold;")
header_item.setSizeHint(header_label.sizeHint())

# 将表头项插入到 QListWidget 的第一行
list_widget.insertItem(0, header_item)
list_widget.setItemWidget(header_item, header_label)

# 添加其他项目
list_widget.addItem("项目1")
list_widget.addItem("项目2")
list_widget.addItem("项目3")

layout.addWidget(list_widget)
window.setLayout(layout)

window.show()
sys.exit(app.exec_())
