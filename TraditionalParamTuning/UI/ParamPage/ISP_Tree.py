import sys
from PyQt5.QtWidgets import (QWidget, QTreeWidget, QTreeWidgetItem, QApplication, QHBoxLayout, QPushButton, QToolButton)
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt, QSize, QEasingCurve
from PyQt5.QtGui import QIcon

class ButtonToggleOpen(QToolButton):

    def __init__(self):
        super().__init__()
        self.setCheckable(True)                                  
        self.setChecked(True)                                   
        self.setArrowType(Qt.RightArrow)
        self.setAutoRaise(True)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)

class ISP_Tree(QWidget):
    def __init__(self):
        super().__init__()
        self.HLayout = QHBoxLayout(self)
        self.tree=QTreeWidget()
        self.tree.setColumnWidth(0, 1)
        self.tree.setColumnWidth(1, 1)
        self.tree.setHeaderHidden( True )
        self.tree.hide()
        self.HLayout.addWidget(self.tree)

        self.btn_toggle_open = ButtonToggleOpen()                                     
        self.HLayout.addWidget(self.btn_toggle_open)

        self.btn_toggle_open.clicked.connect(self.toggle_open)

    def reset_UI(self):
        self.tree.clear()

    def update_UI(self, data):
        self.reset_UI()
        for root in data:
            parent=QTreeWidgetItem(self.tree)
            parent.setText(0, root)
            parent.setExpanded(True)
            # root.setCheckState(0, Qt.Checked)
            self.tree.addTopLevelItem(parent)
            for key in data[root]:
                child=QTreeWidgetItem()
                child.setText(0,key)
                # child.setCheckState(0, Qt.Checked)
                parent.addChild(child)

    def toggle_open(self):
        if self.btn_toggle_open.isChecked():
            self.tree.hide()
            self.btn_toggle_open.setArrowType(Qt.RightArrow)
        else:
            self.tree.show()
            self.btn_toggle_open.setArrowType(Qt.LeftArrow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tree = ISP_Tree({})
    tree.show()
    sys.exit(app.exec_())