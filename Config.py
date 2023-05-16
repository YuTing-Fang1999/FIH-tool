from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle
)
from NTU.sharpness.controller import MainWindow_controller as SharpnessWidget
from NTU.colorcheck.controller import MainWindow_controller as ColorcheckWidget
# from NTU.perceptual_distance.controller import MainWindow_controller as PerceptualDistancekWidget
from NTU.fft.controller import MainWindow_controller as FFTWidget
# from NTU.dxo_dead_leaves.controller import MainWindow_controller as DXO_DFWidget
from QUL.OTPgolden.MyWidget import MyWidget as OTPgoldenWidget

class Config():
    def __init__(self) -> None:
        self.main_config = \
        {
            "QCT": { 
                "AE":{
                    "Calibration":[
                        {
                            "name": "LSC分析小工具",
                            "instruction": QLabel("LSC golden: 將LSC golden資料轉換成高通C7讀檔格式"),
                            "widget": QLabel("LSC分析小工具"),
                        },
                    ],
                    "Tuning":[
                        {
                            "name": "GM2_分析",
                            "instruction": QLabel("LSC 補償:調整 LSC 補償程度並將資料轉成高通C7讀檔格式"),
                            "widget": QLabel("GM2_分析"),
                        },
                    ]
                },
                "CCM":{
                    "Tuning":[
                        {
                            "name": "CCMsimulator",
                            "instruction": QLabel("評估各顏色的Δlightness, Δchroma, Δhue並微調r_gain, b_gain, AWB, 亮度，後求CCM矩陣"),
                            "widget": QLabel("CCMsimulator"),
                        },
                    ]
                },
            },
            "MTK": { 
                "AE":{
                    "Tuning":[
                        {
                            "name": "gammaSimulator_MTK",
                            "instruction": QLabel("調整gamma"),
                            "widget": QLabel("gammaSimulator_MTK"),
                            
                        },
                    ]
                },
            },
                    
                    # "AE2":{
                    #     "Calibration2":[
                    #         {
                    #             "name": "OTPgolden22",
                    #             "widget": OTPgoldenWidget(),
                    #             "instruction": QLabel("OTPgolden instruction")
                    #         },
                    #         {
                    #             "name": "QUL AE222",
                    #             "widget": QLabel("QUL AE2"),
                    #             "instruction": QLabel("QUL AE2 instruction")
                    #         },
                    #     ]
                    # }
        }
            # { 
            #     "name": "MTK",
            #     "navigation_list":
            #     [
            #         {
            #             "name": "AE",
            #             "widget_list":[
            #                 {
            #                     "name": "MTK AE1",
            #                     "widget": QLabel("MTK AE1")
            #                 },
            #                 {
            #                     "name": "MTK AE2",
            #                     "widget": QTextEdit("MTK AE2")
            #                 },
            #             ]
            #         },
            #         {
            #             "name": "AF",
            #             "widget_list":[
            #                 {
            #                     "name": "MTK AF1",
            #                     "widget": QLabel("MTK AF1")
            #                 },
            #                 {
            #                     "name": "MTK AF2",
            #                     "widget": QLabel("MTK AF2")
            #                 },
            #             ]
            #         },
            #     ]
            # },
            
            # { 
            #     "name": "NTU",
            #     "navigation_list":
            #     [
            #         {
            #             "name": "NTU",
            #             "widget_list":[
            #                 {
            #                     "name": "sharpness",
            #                     "widget": SharpnessWidget(),
            #                     "instruction": QLabel("sharpness instruction")
            #                 },
            #                 {
            #                     "name": "colorcheck",
            #                     "widget": ColorcheckWidget(),
            #                     "instruction": QLabel("colorcheck instruction")
            #                 },
            #                 # {
            #                 #     "name": "perceptual_distance",
            #                 #     "widget": PerceptualDistancekWidget()
            #                 # },
            #                 {
            #                     "name": "fft",
            #                     "widget": FFTWidget(),
            #                     "instruction": QLabel("fft instruction")
            #                 },
            #                 # {
            #                 #     "name": "dxo_dead_leaves",
            #                 #     "widget": DXO_DFWidget()
            #                 # }
            #             ]
            #         }
            #     ]
            # },
        # ]
