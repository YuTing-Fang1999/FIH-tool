from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle
)
from PyQt5.QtCore import Qt
from NTU.sharpness.controller import MainWindow_controller as SharpnessWidget
from NTU.colorcheck.controller import MainWindow_controller as ColorcheckWidget
# from NTU.perceptual_distance.controller import MainWindow_controller as PerceptualDistancekWidget
from NTU.fft.controller import MainWindow_controller as FFTWidget
# from NTU.Tuning4.controller import MainWindow_controller as Tuning4Widget
# from NTU.dxo_dead_leaves.controller import MainWindow_controller as DXO_DFWidget
from QUL.LSC.MyWidget import MyWidget as OTPgoldenWidget
from QUL.GM2.MyWidget import MyWidget as GM2Widget
from QUL.AEsimulator.colorChecker.MyWidget import MyWidget as colorCheckerWidget
from QUL.AEsimulator.verifyColorChecker.MyWidget import MyWidget as verifyColorCheckerWidget

class MyLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)

class Config():
    def __init__(self) -> None:
        self.main_config = \
        {
            "Qualcomm": { 
                "AE":{
                    "Calibration":[
                        {
                            "name": "LSC分析小工具",
                            "instruction": MyLabel("LSC golden: 將LSC golden資料轉換成高通C7讀檔格式"),
                            "widget": OTPgoldenWidget(),
                        },
                        # {
                        #     "name": "LSC分析小工具2",
                        #     "instruction": MyLabel("LSC2"),
                        #     "widget": MyLabel("LSC2"),
                        # },
                    ],
                    "Tuning":[
                        {
                            "name": "GM2_分析",
                            "instruction": MyLabel("LSC 補償:調整 LSC 補償程度並將資料轉成高通C7讀檔格式"),
                            "widget": GM2Widget(),
                        },
                        {
                            "name": "colorChecker\n(求luma target)",
                            "instruction": MyLabel("求luma target"),
                            "widget": colorCheckerWidget(),
                        },
                        {
                            "name": "verifyColorChecker",
                            "instruction": MyLabel("驗證colorChecker"),
                            "widget": verifyColorCheckerWidget(),
                        },
                    ]
                },
                "CCM":{
                    "Tuning":[
                        {
                            "name": "CCMsimulator",
                            "instruction": MyLabel("評估各顏色的Δlightness, Δchroma, Δhue並微調r_gain, b_gain, AWB, 亮度，後求CCM矩陣"),
                            "widget": MyLabel("CCMsimulator"),
                        },
                    ],
                    "Analysis":[
                        {
                            "name": "colorCheckerAnalysis",
                            "instruction": MyLabel("評估AWB、CCM"),
                            "widget": MyLabel("colorCheckerAnalysis"),
                        }
                    ]
                },
            },
            "MTK": { 
                "AE":{
                    "Tuning":[
                        {
                            "name": "gammaSimulator_MTK",
                            "instruction": MyLabel("調整gamma"),
                            "widget": MyLabel("gammaSimulator_MTK"),
                            
                        },
                        {
                            "name": "mtkAEanalysis",
                            "instruction": MyLabel("調整 main_target、middle_tone、bright_tone….."),
                            "widget": MyLabel("mtkAEanalysis"),
                            
                        },
                        {
                            "name": "mtkFaceAEanalysis",
                            "instruction": MyLabel("針對人臉AE做調整 main_target、middle_tone、bright_tone….."),
                            "widget": MyLabel("mtkFaceAEanalysis"),
                            
                        },
                    ],
                    "Analysis":[
                        {
                            "name": "mtkAEclassify",
                            "instruction": MyLabel("照片打中的region分類"),
                            "widget": MyLabel("mtkAEclassify"),
                        }
                    ]
                },
                "AWB":{
                    "Tuning":[
                        {
                            "name": "CCMsimulator",
                            "instruction": MyLabel("評估各顏色的Δlightness, Δchroma, Δhue並微調r_gain, b_gain, AWB, 亮度後，調整CCM"),
                            "widget": MyLabel("CCMsimulator"),
                        },
                    ],
                    "Analysis":[
                        {
                            "name": "colorCalculate",
                            "instruction": MyLabel("評估AWB、CCM"),
                            "widget": MyLabel("colorCalculate"),
                        }
                    ]
                }
            },
            # "NTU": { 
            #     "NTU":{
            #         "參數推薦(傳統算法)":[
            #             {
            #                 "name": "參數推薦(傳統算法)",
            #                 "instruction": MyLabel("參數推薦(傳統算法)"),
            #                 "widget": Tuning4Widget(),
                            
            #             },
            #         ],
            #     },
            # },
                    
                    # "AE2":{
                    #     "Calibration2":[
                    #         {
                    #             "name": "OTPgolden22",
                    #             "widget": OTPgoldenWidget(),
                    #             "instruction": MyLabel("OTPgolden instruction")
                    #         },
                    #         {
                    #             "name": "QUL AE222",
                    #             "widget": MyLabel("QUL AE2"),
                    #             "instruction": MyLabel("QUL AE2 instruction")
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
            #                     "widget": MyLabel("MTK AE1")
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
            #                     "widget": MyLabel("MTK AF1")
            #                 },
            #                 {
            #                     "name": "MTK AF2",
            #                     "widget": MyLabel("MTK AF2")
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
            #                     "instruction": MyLabel("sharpness instruction")
            #                 },
            #                 {
            #                     "name": "colorcheck",
            #                     "widget": ColorcheckWidget(),
            #                     "instruction": MyLabel("colorcheck instruction")
            #                 },
            #                 # {
            #                 #     "name": "perceptual_distance",
            #                 #     "widget": PerceptualDistancekWidget()
            #                 # },
            #                 {
            #                     "name": "fft",
            #                     "widget": FFTWidget(),
            #                     "instruction": MyLabel("fft instruction")
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
