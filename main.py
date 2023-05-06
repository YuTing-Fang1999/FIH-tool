from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSizePolicy
# from PyQt5.QtCore import QRect
# from PyQt5.QtGui import 

class SideNavigation(QListWidget):
    def __init__(self, navigation_list) -> None:
        super().__init__()

        self.btn_page_stack = QStackedWidget()

        for i, config in enumerate(navigation_list):
            print(i, config)
            self.insertItem(i, config["name"])
            widget_list = config["widget_list"]

            btn_page = ButtonPage()
            for widget in widget_list:
                btn_page.addBtn(widget["name"])
            self.btn_page_stack.addWidget(btn_page)

        self.currentRowChanged.connect(self.display_btn_page)

    def display_btn_page(self, idx):
        self.btn_page_stack.setCurrentIndex(idx)

class ButtonPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QBoxLayout(QBoxLayout.LeftToRight, self)
    def addBtn(self, name):

        self.main_layout.addWidget(QPushButton(name))
    

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIH整合tool')
        

        main_config = \
        [
            { 
                "name": "MTK",
                "navigation_list":
                [
                    {
                        "name": "MTK0",
                        "widget_list":[
                            {
                                "name": "b0",
                                "widget": QLabel("b0")
                            },
                            {
                                "name": "b0",
                                "widget": QLabel("b0")
                            },
                        ]
                    },
                ]
            },
            { 
                "name": "MTK2",
                "navigation_list":
                [
                    {
                        "name": "MTK2",
                        "widget_list":[
                            {
                                "name": "b2",
                                "widget": QLabel("b0")
                            },
                            {
                                "name": "b2",
                                "widget": QLabel("b0")
                            },
                        ]
                    },
                ]
            }
        ]

        main_layout = QVBoxLayout(self)
        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.side_navigation_stack = QStackedWidget()
        self.btn_page_stack = QStackedWidget()

        for i, each_config in enumerate(main_config):
            button = QPushButton(each_config["name"])
            button.clicked.connect(lambda checked, i=i: self.set_side_navigation_stack(i))
            top_layout.addWidget(button)

            side_navigation = SideNavigation(each_config["navigation_list"])
            self.btn_page_stack.addWidget(side_navigation.btn_page_stack)
            self.side_navigation_stack.addWidget(side_navigation)


        
        bottom_layout.addWidget(self.side_navigation_stack)
        bottom_layout.addWidget(self.btn_page_stack)
        bottom_layout.setStretch(0,1)
        bottom_layout.setStretch(1,8)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)


    def set_side_navigation_stack(self, idx):
        self.btn_page_stack.setCurrentIndex(idx)
        self.side_navigation_stack.setCurrentIndex(idx)

        

if __name__ == '__main__':
    app = QApplication([])
    widget = MyWidget()
    widget.showMaximized()
    app.exec_()