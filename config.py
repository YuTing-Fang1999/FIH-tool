from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle
)

class Config():
    def __init__(self) -> None:
        self.main_config = \
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
                                "widget": QTextEdit("MTK AE2")
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