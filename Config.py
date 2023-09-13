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

from MTK.AE.mtkFaceAEanalysis.MyWidget import MyWidget as mtkFaceAEanalysisWidget
from MTK.AE.mtkFaceAEanalysis.Intro import Intro as mtkFaceAEanalysisIntro
from MTK.AE.mtkAEclassify.MyWidget import MyWidget as mtkAEclassifyWidget
from MTK.AE.mtkAEclassify.Intro import Intro as mtkAEclassifyIntro
from MTK.AE.mtkAEanalysis.MyWidget import MyWidget as mtkAEanalysisWidget
from MTK.AE.mtkAEanalysis.Intro import Intro as mtkAEanalysisIntro

from MTK.AF.MyWidget import MyWidget as MTK_AFWidget
from MTK.AF.Intro import Intro as MTK_AFIntro

from QUL.AF.MyWidget import MyWidget as QUL_AFWidget
from QUL.AF.Intro import Intro as QUL_AFIntro

from QUL.AEsimulator.stepChart.MyWidget import MyWidget as stepChartWidget
from QUL.AEsimulator.stepChart.Intro import Intro as stepChartIntro
from QUL.AEsimulator.verifyGamma.MyWidget import MyWidget as verifyGammaWidget
from QUL.AEsimulator.verifyGamma.Intro import Intro as verifyGammaIntro
# from myPackage.OpenToolBtn import OpenToolBtn
from NTU.ML.MLGenDataset.MyWidget import MyWidget as MLGenDatasetWidget
from NTU.ML.MLGenDataset.Intro import Intro as MLGenDatasetIntro
from NTU.ML.MLAlignDataset.MyWidget import MyWidget as MLAlignDatasetWidget
from NTU.ML.MLAlignDataset.Intro import Intro as MLAlignDatasetIntro
from NTU.ML.MLTrain.Intro import Intro as MLTrainIntro
from NTU.ML.MLRecommand.Intro import Intro as MLRecommandIntro
from NTU.ML.MLPushAndCapture.MyWidget import MyWidget as MLPushAndCaptureWidget
from NTU.ML.MLPushAndCapture.Intro import Intro as MLPushAndCaptureIntro


from TraditionalParamTuning.controller import MainWindow_controller as TraditionalParamTuningWidget
from TraditionalParamTuning.Intro import Intro as TraditionalParamTuningIntro



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
                            "title": "AF log parser",
                            "subtitle": "subtitle",
                            "instruction": QUL_AFIntro(),
                            "widget": QUL_AFWidget(),
                            
                        },
                    ],
                },
                "AE":{
                    "Calibration":[
                        {
                            "title": "LSC分析小工具",
                            "subtitle": "subtitle",
                            "instruction": LSCIntro(),
                            "widget": LSCWidget(),
                        },
                    ],
                    "Tuning":[
                        {
                            "title": "colorChecker\n(求luma target)",
                            "subtitle": "subtitle",
                            "instruction": colorCheckerIntro(),
                            "widget": colorCheckerWidget(),
                        },
                        {
                            "title": "verifyColorChecker",
                            "subtitle": "subtitle",
                            "instruction": verifyColorCheckerIntro(),
                            "widget": verifyColorCheckerWidget(),
                        },
                        {
                            "title": "stepChart\n(計算 Gamma)",
                            "subtitle": "subtitle",
                            "instruction": stepChartIntro(),
                            "widget": stepChartWidget(),
                        },
                        {
                            "title": "verifyStepChart\n(復驗 Gamma)",
                            "subtitle": "subtitle",
                            "instruction": verifyGammaIntro(),
                            "widget": verifyGammaWidget(),
                        },
                    ]
                },
                "CCM":{
                    "Tuning":[
                        {
                            "title": "CCMsimulator",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("評估各顏色的Δlightness, Δchroma, Δhue並微調r_gain, b_gain, AWB, 亮度，後求CCM矩陣"),
                            "widget": MyLabel("CCMsimulator"),
                        },
                    ],
                    "Analysis":[
                        {
                            "title": "colorCheckerAnalysis",
                            "subtitle": "subtitle",
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
                            "title": "AF log parser",
                            "subtitle": "subtitle",
                            "instruction": MTK_AFIntro(),
                            "widget": MTK_AFWidget(),
                            
                        },
                    ],
                },
                "AE":{
                    "Tuning":[
                        {
                            "title": "mtkFaceAEanalysis",
                            "subtitle": "subtitle",
                            "instruction": mtkFaceAEanalysisIntro(),
                            "widget": mtkFaceAEanalysisWidget(),
                            
                        },
                    ],
                    "Analysis":[
                        {
                            "title": "mtkAEclassify",
                            "subtitle": "subtitle",
                            "instruction": mtkAEclassifyIntro(),
                            "widget": mtkAEclassifyWidget(),
                        },
                        {
                            "title": "mtkAEanalysis",
                            "subtitle": "subtitle",
                            "instruction": mtkAEanalysisIntro(),
                            "widget": mtkAEanalysisWidget(),
                        }
                    ]
                },
                "AWB":{
                    "Tuning":[
                        {
                            "title": "CCMsimulator",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("評估各顏色的Δlightness, Δchroma, Δhue並微調r_gain, b_gain, AWB, 亮度後，調整CCM"),
                            "widget": MyLabel("CCMsimulator"),
                        },
                    ],
                    "Analysis":[
                        {
                            "title": "colorCalculate",
                            "subtitle": "subtitle",
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
                            "title": "頻譜分析",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("頻譜分析"),
                            "widget": FFTWidget(),
                            
                        },
                        {
                            "title": "colorcheck",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("colorcheck"),
                            "widget": ColorcheckWidget(),
                            
                        },
                        {
                            "title": "dxo_dead_leaves",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("load 一張 dxo_dead_leaves的照片，會自動偵測ROI計算\n但很容易偵測失敗"),
                            "widget": DXO_DLWidget(),
                            
                        },
                        {
                            "title": "sharpness/noise",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("sharpness/noise"),
                            "widget": SharpnessWidget(),
                            
                        },
                        {
                            "title": "perceptual_distance",
                            "subtitle": "subtitle",
                            "instruction": PerceptualDistancekIntro(),
                            "widget": PerceptualDistancekWidget(),
                            
                        },
                    ],
                    "參數推薦(傳統)":[
                        {
                            "title": "參數推薦(傳統算法)",
                            "subtitle": "subtitle",
                            "instruction": TraditionalParamTuningIntro(),
                            "widget": TraditionalParamTuningWidget(),
                        },
                       
                    ],
                    "參數推薦(ML)":[
                        {
                            "title": "產生資料集",
                            "subtitle": "subtitle",
                            "instruction": MLGenDatasetIntro(),
                            "widget": MLGenDatasetWidget(),
                        },
                        {
                            "title": "對齊資料集",
                            "subtitle": "subtitle",
                            "instruction": MLAlignDatasetIntro(),
                            "widget": MLAlignDatasetWidget(),
                        },
                        {
                            "title": "訓練模型",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("請看教學說明"),
                            "widget": MLTrainIntro(),
                        },
                        {
                            "title": "利用模型做推薦",
                            "subtitle": "subtitle",
                            "instruction": MyLabel("請看教學說明"),
                            "widget": MLRecommandIntro(),
                        },
                        {
                            "title": "推入參數\n拍攝結果照片",
                            "subtitle": "subtitle",
                            "instruction": MLPushAndCaptureIntro(),
                            "widget": MLPushAndCaptureWidget(),
                        }
                    ],
                },
            },
        }