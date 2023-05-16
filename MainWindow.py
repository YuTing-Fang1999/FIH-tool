import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle, QStackedLayout
)
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import 
from Config import Config

class MyStackedLayout(QStackedLayout):
    def __init__(self) -> None:
        super().__init__()
        
    def add_stack_layout(self, stack_layout):
        temp_widget = QWidget()
        temp_widget.setLayout(stack_layout)
        self.addWidget(temp_widget)
        

class ActionList(QListWidget):
    def __init__(self, config) -> None:
        super().__init__()
        
        self.pipeline_stack = MyStackedLayout()
        self.instruction_stack = MyStackedLayout()
        self.widget_stack = MyStackedLayout()
        for i, key in enumerate(config):
            self.addItem(key)
            pipeline_btn = ButtonPage(config[key])
            self.pipeline_stack.addWidget(pipeline_btn)
            self.instruction_stack.add_stack_layout(pipeline_btn.instruction_stack)
            self.widget_stack.add_stack_layout(pipeline_btn.widget_stack)
        
        self.currentRowChanged.connect(self.display_stack)
        self.item(0).setSelected(True)

    def display_stack(self, i):
        self.pipeline_stack.setCurrentIndex(i)
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)
            
class FunctionList(QListWidget):
    def __init__(self, config) -> None:
        super().__init__()
        
        self.action_stack = MyStackedLayout()
        self.pipeline_stack = MyStackedLayout()
        self.instruction_stack = MyStackedLayout()
        self.widget_stack = MyStackedLayout()
        for i, key in enumerate(config):
            self.addItem(key)
            action_list = ActionList(config[key])
            self.action_stack.addWidget(action_list)
            self.pipeline_stack.add_stack_layout(action_list.pipeline_stack)
            self.instruction_stack.add_stack_layout(action_list.instruction_stack)
            self.widget_stack.add_stack_layout(action_list.widget_stack)
        
        self.currentRowChanged.connect(self.display_stack)
        self.item(0).setSelected(True)

    def display_stack(self, i):
        self.action_stack.setCurrentIndex(i)
        self.pipeline_stack.setCurrentIndex(i)
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)
            
        
class StyleBytton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(150, 50)
        
class ButtonPage(QWidget):
    def __init__(self, config) -> None:
        super().__init__()
        self.main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) # 從左上角開始排
        
        self.instruction_stack = MyStackedLayout()
        self.widget_stack = MyStackedLayout()
        
        self.total_btn_group = QButtonGroup()
        self.total_btn_group.setExclusive(True)
        for i, widget_config in enumerate(config):
            btn = StyleBytton(widget_config["name"])
            btn.setCheckable(True)
            if i==0: btn.setChecked(True)
            if i!=0: self.addRightArowLabel()
            self.total_btn_group.addButton(btn)
            btn.clicked.connect(lambda checked, i=i: self.display_stack(i))
            self.addBtn(btn)
            self.instruction_stack.addWidget(widget_config["instruction"])
            self.widget_stack.addWidget(widget_config["widget"])
            
    def display_stack(self, i):
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)

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
        
    def add_stack_layout(self, stack_layout):
        temp_widget = QWidget()
        temp_widget.setLayout(stack_layout)
        self.addWidget(temp_widget)

    
class ToolSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.function_stack = MyStackedLayout()
        self.action_stack = MyStackedLayout()
        self.pipeline_stack = MyStackedLayout()
        
        main_layout = QVBoxLayout(self)
        self.platform_layout = QHBoxLayout()
        
        splitter = StyleSplitter()
        splitter.setOrientation(Qt.Horizontal)
        splitter.add_stack_layout(self.function_stack)
        splitter.add_stack_layout(self.action_stack)
        splitter.add_stack_layout(self.pipeline_stack)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,1)
        splitter.setStretchFactor(2,10)
        
        main_layout.addLayout(self.platform_layout)
        main_layout.addWidget(splitter)
        
    def add_function(self, widget):
        self.function_stack.addWidget(widget)
        
class WidgetDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.instruction_stack = MyStackedLayout()
        self.widget_stack = MyStackedLayout()
        
        main_layout = QVBoxLayout(self)
        
        splitter = StyleSplitter()
        splitter.setOrientation(Qt.Horizontal)
        splitter.add_stack_layout(self.instruction_stack)
        splitter.add_stack_layout(self.widget_stack)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,8)
        main_layout.addWidget(splitter)
        
    def display_widget(self, i):
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIH整合tool')
        
        main_layout = QVBoxLayout(self)
        self.tool_selection = ToolSelection()
        self.widget_display = WidgetDisplay()
        
        splitter = StyleSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.tool_selection)
        splitter.addWidget(self.widget_display)
        splitter.setStretchFactor(0,1)
        splitter.setStretchFactor(1,30)
        main_layout.addWidget(splitter)
        
        main_config = Config().main_config
        self.tool_selection.platform_btn_group = QButtonGroup() # 要用self!
        self.tool_selection.platform_btn_group.setExclusive(True)
        for i, key in enumerate(main_config):
            button = QPushButton(key)
            button.setCheckable(True)
            if i==0: button.setChecked(True)
            self.tool_selection.platform_btn_group.addButton(button)
            function_list = FunctionList(main_config[key])
            self.tool_selection.function_stack.addWidget(function_list)
            self.tool_selection.action_stack.add_stack_layout(function_list.action_stack)
            self.tool_selection.pipeline_stack.add_stack_layout(function_list.pipeline_stack)
            self.widget_display.instruction_stack.add_stack_layout(function_list.instruction_stack)
            self.widget_display.widget_stack.add_stack_layout(function_list.widget_stack)
            button.clicked.connect(lambda checked, i=i: self.display_stack(i))
            self.tool_selection.platform_layout.addWidget(button)
            
    def display_stack(self, i):
        self.tool_selection.function_stack.setCurrentIndex(i)
        self.tool_selection.action_stack.setCurrentIndex(i)
        self.tool_selection.pipeline_stack.setCurrentIndex(i)
        self.widget_display.instruction_stack.setCurrentIndex(i)
        self.widget_display.widget_stack.setCurrentIndex(i)

        

if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.showMaximized()
    app.exec_()