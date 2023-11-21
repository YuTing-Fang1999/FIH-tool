from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QSplitter, QFrame,
    QLayout, QButtonGroup, QStyle, QStackedWidget, QListWidgetItem, QToolButton, QStyledItemDelegate, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPen, QColor, QPalette, QFont, QIcon, QPixmap, QPainter
from Config import Config

class HLine(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

        # Set the color of the line using style sheet
        # self.setStyleSheet("background-color: rgb(13, 13, 13);")
        
        
class StyleBytton(QPushButton):
    def __init__(self, title, subtitle):
        super().__init__()
        self.title = title
        self.subtitle = subtitle
        self.setFixedSize(250, 80)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
        
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the font and size for the first text
        font1 = QFont("Arial", 14)  # Adjust the font and size as needed
        painter.setFont(font1)
        rect = self.rect()
        rect.adjust(0, -20, 0, 0)
        painter.drawText(rect, Qt.AlignCenter, self.title)

        # Set the font and size for the second text
        font2 = QFont("Arial", 10)  # Adjust the font and size as needed
        painter.setFont(font2)
        rect = self.rect()
        rect.adjust(0, 30, 0, 0)  # Adjust the position of the second text
        painter.drawText(rect, Qt.AlignCenter, self.subtitle)
        
        # self.setStyleSheet(
        #     """
        #     QPushButton {
        #         color:rgb(0, 0, 0);
        #         background-color:rgb(255, 170, 0);
        #         border-radius: 4px;
        #     }
        #     """
        # )
        

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()

class BtnPage(QWidget):
    def __init__(self, config) -> None:
        super().__init__()
        self.main_layout = FlowLayout(self)
        # self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) # 從左上角開始排
        
        self.instruction_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        
        self.total_btn_group = QButtonGroup()
        self.total_btn_group.setExclusive(True)
        for i, widget_config in enumerate(config):
            btn = StyleBytton(widget_config["title"], widget_config["subtitle"])
            btn.setCheckable(True)
            if i==0: btn.setChecked(True)
            # if i!=0: self.addRightArowLabel()
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
        self.setFixedSize(25, 80)
        
        # Get the right arrow icon from the QStyle class
        style = QApplication.style()
        arrow_icon = style.standardIcon(QStyle.SP_MediaPlay)
        # Create a QLabel with the right arrow icon
        self.setPixmap(arrow_icon.pixmap(24, 24)) # set the size of the icon
        self.setAlignment(Qt.AlignCenter)
        
class CustomItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.row() == 0:  # 第一個項目不產生懸停效果
            option.state &= ~QStyle.State_MouseOver
            pen = QPen(QColor(255, 255, 255))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        super().paint(painter, option, index)

class FunctionList(QListWidget):

    def __init__(self, config) -> None:
        super().__init__()
        self.setFixedSize(160, 150)
        # # 設定自訂的 ItemDelegate
        itemDelegate = CustomItemDelegate()
        self.setItemDelegate(itemDelegate)
        # create header
        header_item = QListWidgetItem("Function")
        header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)
        self.insertItem(0, header_item)
        
        self.action_stack = QStackedWidget()
        self.pipeline_stack = QStackedWidget()
        self.instruction_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        for i, key in enumerate(config):
            self.addItem(key)
            action_list = ActionList(config[key])
            ###################
            # action_list.setGeometry(1000, 100, 150,150)
            
            # size_policy = action_list.sizePolicy()
            # size_policy.setHorizontalPolicy(QSizePolicy.Fixed)
            # size_policy.setVerticalPolicy(QSizePolicy.Fixed)
            # action_list.setSizePolicy(size_policy)
            # action_list.setFixedSize(160, 150)
            ####################
            self.action_stack.addWidget(action_list)
            self.pipeline_stack.addWidget(action_list.pipeline_stack)
            self.instruction_stack.addWidget(action_list.instruction_stack)
            self.widget_stack.addWidget(action_list.widget_stack)
        
        self.currentRowChanged.connect(self.display_stack)
        self.item(1).setSelected(True) # 0 是header

    def display_stack(self, i):
        i-=1 # 0 是header
        self.action_stack.setCurrentIndex(i)
        self.pipeline_stack.setCurrentIndex(i)
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)
        
class ActionList(QListWidget):
    def __init__(self, config) -> None:
        super().__init__()
        self.setFixedSize(160, 150)
        # # 設定自訂的 ItemDelegate
        itemDelegate = CustomItemDelegate()
        self.setItemDelegate(itemDelegate)
        # create header
        header_item = QListWidgetItem("Stage")
        header_item.setFlags(header_item.flags() & ~Qt.ItemIsSelectable)
        self.insertItem(0, header_item)
        
        self.pipeline_stack = QStackedWidget()
        self.instruction_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        for i, key in enumerate(config):
            self.addItem(key)
            pipeline_btn = BtnPage(config[key])
            self.pipeline_stack.addWidget(pipeline_btn)
            self.instruction_stack.addWidget(pipeline_btn.instruction_stack)
            self.widget_stack.addWidget(pipeline_btn.widget_stack)
        
        self.currentRowChanged.connect(self.display_stack)
        self.item(1).setSelected(True) # 0 是header

    def display_stack(self, i):
        i-=1 # 0 是header
        self.pipeline_stack.setCurrentIndex(i)
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)
        
class ButtonToggleOpen(QToolButton):

    def __init__(self):
        super().__init__()
        self.setCheckable(True)                                  
        self.setArrowType(Qt.UpArrow)
        self.setAutoRaise(True)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)


class StyleSplitter(QSplitter):
    def __init__(self) -> None:
        super().__init__()
        # self.setStyleSheet(
        #     "QSplitter::handle {"
        #     "   border: 2px solid rgb(13, 13, 13);"
        #     "   border-radius: 4px;"
        #     "   width: 5px;"
        #     "}"
        #     "QSplitter::handle:hover {"
        #     "   background-color: #787878;"
        #     "}"
        # )
    
class ToolSelection(QWidget):
    def __init__(self):
        super().__init__()
        self.function_stack = QStackedWidget()
        self.action_stack = QStackedWidget()
        self.pipeline_stack = QStackedWidget()
        
        main_layout = QVBoxLayout(self)
        self.platform_layout = QHBoxLayout()
        Vplatform_layout = QVBoxLayout()
        Vplatform_layout.addLayout(self.platform_layout)
        Vplatform_layout.addWidget(HLine())
        
        HLayout = QHBoxLayout()
        # splitter.setOrientation(Qt.Horizontal)
        HLayout.addWidget(self.function_stack)
        HLayout.addWidget(self.action_stack)
        HLayout.addWidget(self.pipeline_stack)
        HLayout.setStretch(0,1)
        HLayout.setStretch(1,1)
        HLayout.setStretch(2,30)
        
        main_layout.addLayout(Vplatform_layout)
        main_layout.addLayout(HLayout)
        
    def add_function(self, widget):
        self.function_stack.addWidget(widget)
        
class WidgetDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.instruction_stack = QStackedWidget()
        self.widget_stack = QStackedWidget()
        
        main_layout = QVBoxLayout(self)
        
        self.splitter = StyleSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.widget_stack)
        self.splitter.addWidget(self.instruction_stack)
        # splitter.setStretchFactor(0,1)
        # splitter.setStretchFactor(1,1)
        main_layout.addWidget(self.splitter)
        # main_layout.addWidget(self.widget_stack)
        # main_layout.addWidget(FoldMenu2(self.instruction_stack))
        
    def display_widget(self, i):
        self.instruction_stack.setCurrentIndex(i)
        self.widget_stack.setCurrentIndex(i)

class FoldMenu2(QWidget): # 方向與FoldMenu相反
    def __init__(self, widget):
        super().__init__()
        vLayout = QVBoxLayout(self)

        # # Create the QHBoxLayout
        # btn_layout = QHBoxLayout()
        # self.btn_toggle_open = ButtonToggleOpen()
        # self.btn_toggle_open.setArrowType(Qt.DownArrow)
        # btn_layout.addWidget(self.btn_toggle_open)
        # btn_layout.setAlignment(Qt.AlignRight)

        # vLayout.addLayout(btn_layout)
        # vLayout.addWidget(HLine())
        vLayout.addWidget(widget)
        self.widget = widget

        self.widget.setMinimumHeight(300)
        
        self.btn_toggle_open.clicked.connect(self.toggle_open)
        
    def toggle_open(self):
        if self.btn_toggle_open.isChecked():
            self.widget.hide()
            self.btn_toggle_open.setArrowType(Qt.UpArrow)

        else:
            self.widget.show()
            self.btn_toggle_open.setArrowType(Qt.DownArrow)

        
class FoldMenu(QWidget):
    def __init__(self, widget):
        super().__init__()
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(widget)
        self.widget = widget
        
        # Create the QHBoxLayout
        btn_layout = QHBoxLayout()
        self.btn_toggle_open = ButtonToggleOpen()
        btn_layout.addWidget(self.btn_toggle_open)
        btn_layout.setAlignment(Qt.AlignRight)
        vLayout.addLayout(btn_layout)
        vLayout.addWidget(HLine())
        vLayout.setContentsMargins(0,0,0,0)
        
        self.btn_toggle_open.clicked.connect(self.toggle_open)
        
    def toggle_open(self):
        if self.btn_toggle_open.isChecked():
            self.widget.hide()
            self.btn_toggle_open.setArrowType(Qt.DownArrow)
        else:
            self.widget.show()
            self.btn_toggle_open.setArrowType(Qt.UpArrow)

class PlatFormBtn(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.setFixedWidth(160)
        self.setCursor(QCursor(Qt.OpenHandCursor))

        palette = self.palette()
        palette.setColor(QPalette.Button, QColor(0, 0, 255))  # Set blue color for the button

        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIH整合tool')
        
        main_layout = QVBoxLayout(self)
        self.tool_selection = ToolSelection()
        self.widget_display = WidgetDisplay()
        
        main_config = Config().main_config
        self.tool_selection.platform_btn_group = QButtonGroup() # 要用self!
        self.tool_selection.platform_btn_group.setExclusive(True)
        for i, key in enumerate(main_config):
            button = PlatFormBtn(key)
            button.setCheckable(True)
            if i==0: button.setChecked(True)
            self.tool_selection.platform_btn_group.addButton(button)
            function_list = FunctionList(main_config[key])
            ############################
            # function_list.setGeometry(1000, 100, 150, 150)
            # print("f")
            # size_policy = function_list.sizePolicy()
            # size_policy.setHorizontalPolicy(QSizePolicy.Fixed)
            # size_policy.setVerticalPolicy(QSizePolicy.Fixed)
            # function_list.setSizePolicy(size_policy)
            # function_list.setFixedSize(160, 150)
            #############################
            self.tool_selection.function_stack.addWidget(function_list)
            self.tool_selection.action_stack.addWidget(function_list.action_stack)
            self.tool_selection.pipeline_stack.addWidget(function_list.pipeline_stack)
            self.widget_display.instruction_stack.addWidget(function_list.instruction_stack)
            self.widget_display.widget_stack.addWidget(function_list.widget_stack)
            button.clicked.connect(lambda checked, i=i: self.display_stack(i))
            self.tool_selection.platform_layout.addWidget(button)
        self.tool_selection.platform_layout.addWidget(button)
        spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.tool_selection.platform_layout.addItem(spacerItem)

        # splitter = StyleSplitter()
        # splitter.setOrientation(Qt.Vertical)
        # splitter.addWidget(FoldMenu(self.tool_selection))
        # splitter.addWidget(self.widget_display)
        # splitter.setStretchFactor(1,1)
        # main_layout.addWidget(splitter)
        main_layout.addWidget(FoldMenu(self.tool_selection))
        main_layout.addWidget(self.widget_display)
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 100)

        self.set_style()
            
    def display_stack(self, i):
        self.tool_selection.function_stack.setCurrentIndex(i)
        self.tool_selection.action_stack.setCurrentIndex(i)
        self.tool_selection.pipeline_stack.setCurrentIndex(i)
        self.widget_display.instruction_stack.setCurrentIndex(i)
        self.widget_display.widget_stack.setCurrentIndex(i)

    def set_style(self):
        # # 创建一个QPalette对象
        # palette = self.palette()

        # # 设置QPalette的背景色
        # palette.setColor(QPalette.Background, QColor(58, 57, 55))
        
        # # 将QPalette应用到窗口
        # self.setPalette(palette)

        self.setStyleSheet(
            # background-color: rgb(58, 57, 55);
            # color: rgb(255, 255, 255);
            """
            font-family:微軟正黑體;
            font-weight: bold;
            font-size: 12pt;
            """
        )
        
    def closeEvent(self, event):
        # TraditionalParamTuning = self.widget_display.widget_stack.widget(2).widget(0).widget(1).widget(0)
        # print(TraditionalParamTuning)
        # TraditionalParamTuning.close()
        print("closeEvent MainWindow")
        super(MainWindow, self).closeEvent(event)

        

if __name__ == '__main__':
    app = QApplication([])
    widget = MainWindow()
    widget.showMaximized()
    app.exec_()