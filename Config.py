from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from NTU.sharpness.controller import MainWindow_controller as SharpnessWidget
from NTU.colorcheck.controller import MainWindow_controller as ColorcheckWidget
from NTU.fft.controller import MainWindow_controller as FFTWidget
from NTU.perceptual_distance.controller import MainWindow_controller as PerceptualDistancekWidget
from NTU.perceptual_distance.Intro import Intro as PerceptualDistancekIntro
from NTU.dxo_dead_leaves.controller import MainWindow_controller as DXO_DLWidget
from NTU.Chou.ex import MyWidget as PhotoDiff_Widget
from NTU.Chou.Intro import Intro as PhotoDiff_Intro

from QC.AE.Analysis.LSC.MyWidget import MyWidget as LSCWidget
from QC.AE.Analysis.LSC.Intro import Intro as LSCIntro

from QC.AE.Calibration.colorChecker.MyWidget import MyWidget as colorCheckerWidget
from QC.AE.Calibration.colorChecker.Intro import Intro as colorCheckerIntro
from QC.AE.Calibration.verifyColorChecker.MyWidget import MyWidget as verifyColorCheckerWidget
from QC.AE.Calibration.verifyColorChecker.Intro import Intro as verifyColorCheckerIntro
from QC.AE.Calibration.stepChart.MyWidget import MyWidget as stepChartWidget
from QC.AE.Calibration.stepChart.Intro import Intro as stepChartIntro
from QC.AE.Calibration.verifyStepChart.MyWidget import MyWidget as verifyStepChartWidget
from QC.AE.Calibration.verifyStepChart.Intro import Intro as verifyStepChartIntro

from QC.AF.Analysis.AFLogFetcher.MyWidget import MyWidget as QC_AFWidget
from QC.AF.Analysis.AFLogFetcher.Intro import Intro as QC_AFIntro
from QC.AF.Analysis.PhotoFocusFilter.UX import MyWidget as QC_AFPhotoFocusFilterWidget
from QC.AF.Analysis.PhotoFocusFilter.Intro import Intro as QC_AFPhotoFocusFilterIntro
from QC.AF.Analysis.FocusFilter_Laplacian.UX import MyWidget as QC_AFFocusFilterLaplacainWidget
from QC.AF.Analysis.FocusFilter_Laplacian.Intro import Intro as QC_AFFocusFilterLaplacainIntro

from QC.AWB.Calibration.CCMCVInitializer.MyWidget import MyWidget as CCMCVInitializerWidget
from QC.AWB.Calibration.CCMCVInitializer.Intro import Intro as CCMCVInitializerIntro

from QC.ISP.Analysis.KeywordISOSorter.MyWidget import MyWidget as QC_KeywordISOSorterWidget
from QC.ISP.Analysis.KeywordISOSorter.Intro import Intro as QC_KeywordISOSorterIntro

from MTK.AE.Tuning.mtkFaceAEanalysis.MyWidget import MyWidget as mtkFaceAEanalysisWidget
from MTK.AE.Tuning.mtkFaceAEanalysis.Intro import Intro as mtkFaceAEanalysisIntro
from MTK.AE.Analysis.mtkAEclassify.MyWidget import MyWidget as mtkAEclassifyWidget
from MTK.AE.Analysis.mtkAEclassify.Intro import Intro as mtkAEclassifyIntro
from MTK.AE.Analysis.mtkAEanalysis.MyWidget import MyWidget as mtkAEanalysisWidget
from MTK.AE.Analysis.mtkAEanalysis.Intro import Intro as mtkAEanalysisIntro
from MTK.AE.Analysis.ToneCategorizer.ToneWidget import MyWidget as ToneCategorizerWidget
from MTK.AE.Analysis.ToneCategorizer.Intro import Intro as ToneCategorizerIntro

from MTK.AF.Analysis.AFLogFetcher.MyWidget import MyWidget as MTK_AFWidget
from MTK.AF.Analysis.AFLogFetcher.Intro import Intro as MTK_AFIntro
from MTK.AF.Analysis.PhotoFocusFilter.UX import MyWidget as MTK_AFPhotoFocusFilterWidget
from MTK.AF.Analysis.PhotoFocusFilter.Intro import Intro as MTK_AFPhotoFocusFilterIntro
from MTK.AF.Analysis.FocusFilter_Laplacian.UX import MyWidget as MTK_AFFocusFilterLaplacainWidget
from MTK.AF.Analysis.FocusFilter_Laplacian.Intro import Intro as MTK_AFFocusFilterLaplacainIntro

from MTK.ISP.Analysis.KeywordISOSorter.MyWidget import MyWidget as MTK_KeywordISOSorterWidget
from MTK.ISP.Analysis.KeywordISOSorter.Intro import Intro as MTK_KeywordISOSorterIntro

from NTU.ML.MyWidget import MyWidget as MLWidget
from NTU.ML.Intro import Intro as MLIntro

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
                "QC": {
                    "AF": {
                        "Analysis": [
                            {
                                "title": "AF Log Fetcher",
                                "subtitle": "Fetch and sort logs",
                                "instruction": QC_AFIntro(),
                                "widget": QC_AFWidget(),

                            },
                            {
                                "title": "Photo Focus Filter",
                                "subtitle": "Filter for blurry images",
                                "instruction": QC_AFPhotoFocusFilterIntro(),
                                "widget": QC_AFPhotoFocusFilterWidget(),

                            },
                            {
                                "title": "Focus Filter (Laplacian)",
                                "subtitle": "Filter for blurry images with threshold",
                                "instruction": QC_AFFocusFilterLaplacainIntro(),
                                "widget": QC_AFFocusFilterLaplacainWidget(),

                            },
                        ],
                    },
                    "AE": {
                        "Analysis": [
                            {
                                "title": "Shading Shape Display",
                                "subtitle": "Visualizing lens shading data",
                                "instruction": LSCIntro(),
                                "widget": LSCWidget(),
                            },
                            # {
                            #     "title": "Brightness Comparator",
                            #     "subtitle": "Compare ratio, histograms & simulate",
                            #     "instruction": MyLabel(""),
                            #     "widget": MyLabel(""),

                            # },
                        ],
                        "Calibration": [
                            {
                                "title": "Luma Target Initializer",
                                "subtitle": "Luma Tuning via Color Checker",
                                "instruction": colorCheckerIntro(),
                                "widget": colorCheckerWidget(),
                            },
                            {
                                "title": "Luma Target Verifier",
                                "subtitle": "Compute delta Y via Color Checker",
                                "instruction": verifyColorCheckerIntro(),
                                "widget": verifyColorCheckerWidget(),
                            },
                            {
                                "title": "Gamma15 Initializer",
                                "subtitle": "Gamma Tuning via Step Chart",
                                "instruction": stepChartIntro(),
                                "widget": stepChartWidget(),
                            },
                            {
                                "title": "Gamma Verifier",
                                "subtitle": "Compute delta Y via Step Chart",
                                "instruction": verifyStepChartIntro(),
                                "widget": verifyStepChartWidget(),
                            },
                        ]
                    },
                    "AWB": {
                        "Calibration": [
                            {
                                "title": "CCM/CV Initializer",
                                "subtitle": "CCM/CV calibration via Color Checker",
                                "instruction": CCMCVInitializerIntro(),
                                "widget": CCMCVInitializerWidget(),
                            },
                        ]
                    },
                    "ISP": {
                        "Analysis": [
                            {
                                "title": "Spectrum Grapher",
                                "subtitle": "Display Spectrum and Histogram",
                                "instruction": MyLabel("頻譜分析"),
                                "widget": FFTWidget(),
                            },
                            {
                                "title": "Color Checker SNR",
                                "subtitle": "Comparing YRGB SNR of 24 patch",
                                "instruction": MyLabel("colorcheck"),
                                "widget": ColorcheckWidget(),
                            },
                            {
                                "title": "DL acutance",
                                "subtitle": "DL Acutance via DeadLeaves",
                                "instruction": MyLabel("load 一張 dxo_dead_leaves的照片，會自動偵測ROI計算"),
                                "widget": DXO_DLWidget(),
                            },
                            {
                                "title": "ISP Metrics Calculator",
                                "subtitle": "Calculate sharpness and noise values",
                                "instruction": MyLabel("sharpness/noise"),
                                "widget": SharpnessWidget(),
                            },
                            {
                                "title": "Perceptual Distance",
                                "subtitle": "Compute perceputal distance",
                                "instruction": PerceptualDistancekIntro(),
                                "widget": PerceptualDistancekWidget(),
                            },
                            {
                                "title": "Keyword ISO Sorter",
                                "subtitle": "Rename, sort by keyword ISO",
                                "instruction": QC_KeywordISOSorterIntro(),
                                "widget": QC_KeywordISOSorterWidget(),
                            },
                        ],
                        "Tuning": [
                            {
                                "title": "ISP Auto Tune (Basic)",
                                "subtitle": "Recommended ISP param",
                                "instruction": TraditionalParamTuningIntro(),
                                "widget": TraditionalParamTuningWidget(),
                            },
                            {
                                "title": "ISP Auto Tune (ML)",
                                "subtitle": "Recommended ISP param",
                                "instruction": MLIntro(),
                                "widget": MLWidget(),
                            },
                        ]
                    },
                },
                "MTK": {
                    "AF": {
                        "Analysis": [
                            {
                                "title": "AF Log Fetcher",
                                "subtitle": "Fetch and sort logs",
                                "instruction": MTK_AFIntro(),
                                "widget": MTK_AFWidget(),

                            },
                            {
                                "title": "Photo Focus Filter",
                                "subtitle": "Filter for blurry images",
                                "instruction": MTK_AFPhotoFocusFilterIntro(),
                                "widget": MTK_AFPhotoFocusFilterWidget(),

                            },
                            {
                                "title": "Focus Filter (Laplacian)",
                                "subtitle": "Filter for blurry images with threshold",
                                "instruction": MTK_AFFocusFilterLaplacainIntro(),
                                "widget": MTK_AFFocusFilterLaplacainWidget(),

                            },
                        ],
                    },
                    "AE": {
                        "Analysis": [
                            {
                                "title": "Tone Categorizer",
                                "subtitle": "Classify & lookup with LV, DR",
                                "instruction": ToneCategorizerIntro(),
                                "widget": ToneCategorizerWidget(),

                            },
                            {
                                "title": "AE Classify Mapper",
                                "subtitle": "For Weighting & THD tuning",
                                "instruction": mtkAEclassifyIntro(),
                                "widget": mtkAEclassifyWidget(),
                            },
                            {
                                "title": "AE Metrics Analyzer",
                                "subtitle": "Computation of related values",
                                "instruction": mtkAEanalysisIntro(),
                                "widget": mtkAEanalysisWidget(),
                            },
                            {
                                "title": "PhotoDiff",
                                "subtitle": "Diff in AE and AWB Target",
                                "instruction": PhotoDiff_Intro(),
                                "widget": PhotoDiff_Widget(),
                            },
                        ],
                        "Tuning": [
                            {
                                "title": "Face AE Tuner",
                                "subtitle": "Adjust Face link target param",
                                "instruction": mtkFaceAEanalysisIntro(),
                                "widget": mtkFaceAEanalysisWidget(),

                            },
                        ],

                    },
                    # "AWB": {
                    #     "Analysis": [
                    #         {
                    #             "title": "Preference Gain Optimizer",
                    #             "subtitle": "For preference gain tuning",
                    #             "instruction": MyLabel(""),
                    #             "widget": MyLabel(""),
                    #         }
                    #     ],
                    # },
                    "ISP": {
                        "Analysis": [
                            {
                                "title": "Spectrum Grapher",
                                "subtitle": "Display Spectrum and Histogram",
                                "instruction": MyLabel("頻譜分析"),
                                "widget": FFTWidget(),
                            },
                            {
                                "title": "Color Checker SNR",
                                "subtitle": "Comparing YRGB SNR of 24 patch",
                                "instruction": MyLabel("colorcheck"),
                                "widget": ColorcheckWidget(),
                            },
                            {
                                "title": "DL acutance",
                                "subtitle": "DL Acutance via DeadLeaves",
                                "instruction": MyLabel("load 一張 dxo_dead_leaves的照片，會自動偵測ROI計算\n但很容易偵測失敗"),
                                "widget": DXO_DLWidget(),
                            },
                            {
                                "title": "ISP Metrics Calculator",
                                "subtitle": "Calculate sharpness and noise values",
                                "instruction": MyLabel("sharpness/noise"),
                                "widget": SharpnessWidget(),
                            },
                            {
                                "title": "Perceptual Distance",
                                "subtitle": "Compute perceputal distance",
                                "instruction": PerceptualDistancekIntro(),
                                "widget": PerceptualDistancekWidget(),
                            },
                            {
                                "title": "Keyword ISO Sorter",
                                "subtitle": "Rename, sort by keyword ISO",
                                "instruction": MTK_KeywordISOSorterIntro(),
                                "widget": MTK_KeywordISOSorterWidget(),
                            },
                        ],
                    }
                }
            }
