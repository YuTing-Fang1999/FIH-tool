from PyQt5.QtWidgets import (
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QSpacerItem, QSizePolicy, QScrollArea, QLabel
)
from PyQt5.QtCore import Qt

from .TriggerSelector import TriggerSelector
from .ParamModifyBlock import ParamModifyBlock
from .ParamRangeBlock import ParamRangeBlock
from .HyperSettingBlock import HyperSettingBlock
from .PushAndSaveBlock import PushAndSaveBlock
from .ISP_Tree import ISP_Tree

import os
import xml.etree.ElementTree as ET

class ParamPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_UI()
        # self.setup_controller()

    def setup_UI(self):
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        HLayout = QHBoxLayout()

        self.ISP_tree = ISP_Tree()
        HLayout.addWidget(self.ISP_tree)

        ###### Left Part ######
        VLayout = QVBoxLayout()
        VLayout.setContentsMargins(0, 0, 0, 0)

        self.trigger_selector = TriggerSelector()
        VLayout.addWidget(self.trigger_selector)

        self.param_modify_block = ParamModifyBlock()
        VLayout.addWidget(self.param_modify_block)

        self.push_and_save_block = PushAndSaveBlock()
        VLayout.addWidget(self.push_and_save_block)

        VLayout.addItem(spacerItem)
        
        HLayout.addLayout(VLayout)
        ###### Left Part ######

        ###### Middle Part ######
        VLayout = QVBoxLayout()
        self.param_range_block = ParamRangeBlock()
        VLayout.addWidget(self.param_range_block)
        VLayout.addItem(spacerItem)
        HLayout.addLayout(VLayout)
        ###### Middle Part ######

        ###### Right Part ######
        VLayout = QVBoxLayout()
        self.hyper_setting_block = HyperSettingBlock()
        VLayout.addWidget(self.hyper_setting_block)

        VLayout.addItem(spacerItem)
        HLayout.addLayout(VLayout)
        ###### Right Part ######

        #Scroll Area Properties
        scroll_wrapper = QHBoxLayout(self)
        layout_wrapper = QWidget()
        layout_wrapper.setLayout(HLayout)
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True)
        scroll.setWidget(layout_wrapper)
        scroll_wrapper.addWidget(scroll)

        # Set Style
        # self.setStyleSheet(
        #     "QLabel{font-size:12pt; font-family:微軟正黑體; color:white;}"
        #     "QPushButton{font-size:12pt; font-family:微軟正黑體; background-color:rgb(255, 170, 0);}"
        #     "QLineEdit{font-size:10pt; font-family:微軟正黑體; background-color: rgb(255, 255, 255); border: 2px solid gray; border-radius: 5px;}"
        # )
    
    def reset_UI(self):
        self.ISP_tree.reset_UI()
        self.trigger_selector.clear()
        self.param_modify_block.reset_UI()
        self.param_range_block.reset_UI()


    


    
    
       



