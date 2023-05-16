import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle
)
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import 
from Config import Config

class StyleBytton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(150, 50)

class Navigation(QListWidget):
    def __init__(self, navigation_list) -> None:
        super().__init__()

        self.btn_page_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        self.instruction_stack = QStackedWidget()
        self.total_btn_group = QButtonGroup()
        self.total_btn_group.setExclusive(True)
        idx = 0
        for i, config in enumerate(navigation_list):
            self.insertItem(i, config["name"])
            widget_list = config["widget_list"]

            btn_page = ButtonPage()
            for j, widget in enumerate(widget_list):
                btn = StyleBytton(widget["name"])
                btn.setCheckable(True)
                if idx==0: btn.setChecked(True)
                if j!=0: btn_page.addRightArowLabel()
                self.total_btn_group.addButton(btn)
                btn.clicked.connect(lambda checked, idx=idx: self.widget_stack.setCurrentIndex(idx))
                btn.clicked.connect(lambda checked, idx=idx: self.instruction_stack.setCurrentIndex(idx))
                idx+=1
                btn_page.addBtn(btn)
                self.widget_stack.addWidget(widget["widget"])
                self.instruction_stack.addWidget(widget["instruction"])
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
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) # 從左上角開始排

    def addBtn(self, btn):
        self.main_layout.addWidget(btn)
    def addRightArowLabel(self):
        self.main_layout.addWidget(RightArowLabel())

class RightArowLabel(QLabel):
    def __init__(self):
        super().__init__()
        # Get the right arrow icon from the QStyle class
        style = QApplication.style()
        arrow_icon = style.standardIcon(QStyle.SP_MediaPlay)
        # Create a QLabel with the right arrow icon
        self.setPixmap(arrow_icon.pixmap(24, 24)) # set the size of the icon


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

    def setup_stack(self, widget_stack: QStackedWidget, instructions_stack: QStackedWidget):
        self.widget_stack = widget_stack
        self.instructions_stack = instructions_stack

        main_config = Config().main_config
        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        splitter = StyleSplitter()

        self.side_navigation_stack = QStackedWidget()
        self.btn_page_stack = QStackedWidget()

        self.top_btn_group = QButtonGroup()
        self.top_btn_group.setExclusive(True)
        for i, each_config in enumerate(main_config):
            button = QPushButton(each_config["name"])
            button.setCheckable(True)
            if i==0: button.setChecked(True)
            self.top_btn_group.addButton(button)
            button.clicked.connect(lambda checked, i=i: self.set_stack(i))
            top_layout.addWidget(button)

            side_navigation = Navigation(each_config["navigation_list"])
            self.btn_page_stack.addWidget(side_navigation.btn_page_stack)
            self.widget_stack.addWidget(side_navigation.widget_stack)
            self.instructions_stack.addWidget(side_navigation.instruction_stack)
            self.side_navigation_stack.addWidget(side_navigation)
        
        splitter.addWidget(self.side_navigation_stack)
        splitter.addWidget(self.btn_page_stack)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,8)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(splitter)

    def set_stack(self, idx):
        self.widget_stack.setCurrentIndex(idx)
        self.instructions_stack.setCurrentIndex(idx)
        self.btn_page_stack.setCurrentIndex(idx)
        self.side_navigation_stack.setCurrentIndex(idx)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIH整合tool')
        
        main_layout = QVBoxLayout(self)
        self.tool_selection_widget = ToolSelection()
        self.widget_stack = QStackedWidget()
        self.instructions_stack = QStackedWidget()
        self.tool_selection_widget.setup_stack(self.widget_stack)
        self.tool_selection_widget.set_instructions_stack(self.instructions_stack)
        
        buttom_splitter = StyleSplitter()
        buttom_splitter.setOrientation(Qt.Horizontal)
        buttom_splitter.addWidget(self.instructions_stack)
        buttom_splitter.addWidget(self.widget_stack)
        buttom_splitter.setStretchFactor(0,1)
        buttom_splitter.setStretchFactor(1,1)

        splitter = StyleSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.tool_selection_widget)
        splitter.addWidget(buttom_splitter)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,1)
        main_layout.addWidget(splitter)
        

if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.showMaximized()
    app.exec_()