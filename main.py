import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup
)
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import 

class Navigation(QListWidget):
    def __init__(self, navigation_list) -> None:
        super().__init__()

        self.btn_page_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        idx = 0
        for i, config in enumerate(navigation_list):
            self.insertItem(i, config["name"])
            widget_list = config["widget_list"]

            btn_page = ButtonPage()
            for j, widget in enumerate(widget_list):
                btn = QPushButton(widget["name"])
                btn.setCheckable(True)
                if j==0: btn.setChecked(True)
                btn.clicked.connect(lambda checked, idx=idx: self.widget_stack.setCurrentIndex(idx))
                idx+=1
                btn_page.addBtn(btn)
                self.widget_stack.addWidget(widget["widget"])
            self.btn_page_stack.addWidget(btn_page)

        self.currentRowChanged.connect(self.display_btn_page)
        self.item(0).setSelected(True)

    def display_btn_page(self, idx):
        self.btn_page_stack.setCurrentIndex(idx)


# class Button

class ButtonPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(True)
    def addBtn(self, btn):
        self.main_layout.addWidget(btn)
        self.btn_group.addButton(btn)

class StyleSplitter(QSplitter):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            "QSplitter::handle {"
            "   background-color: #c2c2c2;"
            "   border: 1px solid #8f8f91;"
            "   border-radius: 4px;"
            "   width: 5px;"
            "}"
            "QSplitter::handle:hover {"
            "   background-color: #787878;"
            "}"
        )
    
class ToolSelection(QWidget):
    def __init__(self):
        super().__init__()

    def set_widget_stack(self, widget_stack: QStackedWidget):
        self.widget_stack = widget_stack

        main_config = \
        [
            { 
                "name": "MTK",
                "navigation_list":
                [
                    {
                        "name": "AE",
                        "widget_list":[
                            {
                                "name": "MTK AE1",
                                "widget": QLabel("MTK AE1")
                            },
                            {
                                "name": "MTK AE2",
                                "widget": QLabel("MTK AE2")
                            },
                        ]
                    },
                    {
                        "name": "AF",
                        "widget_list":[
                            {
                                "name": "MTK AF1",
                                "widget": QLabel("MTK AF1")
                            },
                            {
                                "name": "MTK AF2",
                                "widget": QLabel("MTK AF2")
                            },
                        ]
                    },
                ]
            },
            { 
                "name": "QUL",
                "navigation_list":
                [
                    {
                        "name": "AE",
                        "widget_list":[
                            {
                                "name": "QUL AE1",
                                "widget": QLabel("QUL AE1")
                            },
                            {
                                "name": "QUL AE2",
                                "widget": QLabel("QUL AE2")
                            },
                        ]
                    },
                ]
            }
        ]


        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        splitter = StyleSplitter()

        self.side_navigation_stack = QStackedWidget()
        self.btn_page_stack = QStackedWidget()

        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(True)
        for i, each_config in enumerate(main_config):
            button = QPushButton(each_config["name"])
            button.setCheckable(True)
            if i==0: button.setChecked(True)
            self.btn_group.addButton(button)
            button.clicked.connect(lambda checked, i=i: self.set_stack(i))
            top_layout.addWidget(button)

            side_navigation = Navigation(each_config["navigation_list"])
            self.btn_page_stack.addWidget(side_navigation.btn_page_stack)
            self.widget_stack.addWidget(side_navigation.widget_stack)
            self.side_navigation_stack.addWidget(side_navigation)
        
        splitter.addWidget(self.side_navigation_stack)
        splitter.addWidget(self.btn_page_stack)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,8)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(splitter)

    def set_stack(self, idx):
        self.widget_stack.setCurrentIndex(idx)
        self.btn_page_stack.setCurrentIndex(idx)
        self.side_navigation_stack.setCurrentIndex(idx)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIH整合tool')
        

        
        main_layout = QVBoxLayout(self)

        splitter = StyleSplitter()
        splitter.setOrientation(Qt.Vertical)

        self.tool_selection_widget = ToolSelection()
        self.widget_stack = QStackedWidget()

        splitter.addWidget(self.tool_selection_widget)
        splitter.addWidget(self.widget_stack)
        self.tool_selection_widget.set_widget_stack(self.widget_stack)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,15)
        main_layout.addWidget(splitter)
        

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.showMaximized()
    app.exec_()