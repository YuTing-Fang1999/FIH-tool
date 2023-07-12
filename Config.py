from PyQt5.QtWidgets import (
    QWidget, QLabel, QApplication, QBoxLayout, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QStackedWidget, QSplitter,
    QTextEdit, QButtonGroup, QStyle
)
from PyQt5.QtCore import Qt
from NTU.sharpness.controller import MainWindow_controller as SharpnessWidget
from NTU.colorcheck.controller import MainWindow_controller as ColorcheckWidget
from NTU.fft.controller import MainWindow_controller as FFTWidget
from NTU.perceptual_distance.controller import MainWindow_controller as PerceptualDistancekWidget
from NTU.perceptual_distance.Intro import Intro as PerceptualDistancekIntro
from NTU.dxo_dead_leaves.controller import MainWindow_controller as DXO_DLWidget
from QUL.LSC.MyWidget import MyWidget as LSCWidget
from QUL.LSC.Intro import Intro as LSCIntro

from QUL.AEsimulator.colorChecker.MyWidget import MyWidget as colorCheckerWidget
from QUL.AEsimulator.colorChecker.Intro import Intro as colorCheckerIntro

from QUL.AEsimulator.verifyColorChecker.MyWidget import MyWidget as verifyColorCheckerWidget
from QUL.AEsimulator.verifyColorChecker.Intro import Intro as verifyColorCheckerIntro

from MTK.AF.MyWidget import MyWidget as MTK_AFWidget
from MTK.AF.Intro import Intro as MTK_AFIntro

from QUL.AF.MyWidget import MyWidget as QUL_AFWidget
from QUL.AF.Intro import Intro as QUL_AFIntro

from QUL.AEsimulator.stepChart.MyWidget import MyWidget as stepChartWidget
from QUL.AEsimulator.stepChart.Intro import Intro as stepChartIntro
from QUL.AEsimulator.verifyGamma.MyWidget import MyWidget as verifyGammaWidget
from QUL.AEsimulator.verifyGamma.Intro import Intro as verifyGammaIntro
from TraditionalParamTuning.controller import MainWindow_controller as TraditionalParamTuningWidget
# from myPackage.OpenToolBtn import OpenToolBtn
from NTU.ML.MLGenDataset.MyWidget import MyWidget as MLGenDatasetWidget
from NTU.ML.MLPushAndCapture.MyWidget import MyWidget as MLPushAndCaptureWidget
from NTU.ML.MLPushAndCapture.Intro import Intro as MLPushAndCaptureIntro


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
                "AF":{
                    "Analysis":[
                        {
                            "name": "AF log parser",
                            "instruction": QUL_AFIntro(),
                            "widget": QUL_AFWidget(),
                            
                        },
                    ],
                },
                "AE":{
                    "Calibration":[
                        {
                            "name": "LSC分析小工具",
                            "instruction": LSCIntro(),
                            "widget": LSCWidget(),
                        },
                    ],
                    "Tuning":[
                        {
                            "name": "colorChecker\n(求luma target)",
                            "instruction": colorCheckerIntro(),
                            "widget": colorCheckerWidget(),
                        },
                        {
                            "name": "verifyColorChecker",
                            "instruction": verifyColorCheckerIntro(),
                            "widget": verifyColorCheckerWidget(),
                        },
                        {
                            "name": "stepChart\n(計算 Gamma)",
                            "instruction": stepChartIntro(),
                            "widget": stepChartWidget(),
                        },
                        {
                            "name": "verifyStepChart\n(復驗 Gamma)",
                            "instruction": verifyGammaIntro(),
                            "widget": verifyGammaWidget(),
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
                "AF":{
                    "Analysis":[
                        {
                            "name": "AF log parser",
                            "instruction": MTK_AFIntro(),
                            "widget": MTK_AFWidget(),
                            
                        },
                    ],
                },
                "AE":{
                    "Tuning":[
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
            "NTU": { 
                "NTU":{
                    "影像分析工具":[
                        {
                            "name": "頻譜分析",
                            "instruction": MyLabel("頻譜分析"),
                            "widget": FFTWidget(),
                            
                        },
                        {
                            "name": "colorcheck",
                            "instruction": MyLabel("colorcheck"),
                            "widget": ColorcheckWidget(),
                            
                        },
                        {
                            "name": "dxo_dead_leaves",
                            "instruction": MyLabel("load 一張 dxo_dead_leaves的照片，會自動偵測ROI計算\n但很容易偵測失敗"),
                            "widget": DXO_DLWidget(),
                            
                        },
                        {
                            "name": "sharpness/noise",
                            "instruction": MyLabel("sharpness/noise"),
                            "widget": SharpnessWidget(),
                            
                        },
                        {
                            "name": "perceptual_distance",
                            "instruction": PerceptualDistancekIntro(),
                            "widget": PerceptualDistancekWidget(),
                            
                        },
                    ],
                    "參數推薦(傳統)":[
                        {
                            "name": "參數推薦(傳統算法)",
                            "instruction": MyLabel("參數推薦(傳統算法)"),
                            "widget": TraditionalParamTuningWidget(),
                        },
                       
                    ],
                    "參數推薦(ML)":[
                        {
                            "name": "產生資料集",
                            "instruction": MyLabel("產生資料集"),
                            "widget": MLGenDatasetWidget(),
                        },
                        {
                            "name": "推入參數\n拍攝結果照片",
                            "instruction": MLPushAndCaptureIntro(),
                            "widget": MLPushAndCaptureWidget(),
                        }
                    ],
                },
            },
                    
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
