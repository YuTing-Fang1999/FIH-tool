from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
1.「Delete」刪除勾選項目 (預設勾選FDStable = 0)
2.「Import AE.cpp」匯入相應調教檔。
3.「Import data folder」須包含測試機照片、測試機exif、參考機照片(檔名範例:1_SX3, 1_SX3.exif, 1_E7.jpg)，開啟後即運算， 該按鈕和CMD可查看進度。
4. 觀察“Before Day”、“Before NS”、“Before Total”等之數值是否異常(正常為數百)，若異常則進行步驟9。
5.「Optimize」最佳化參數(可按數次結果可能不同)。
6.「Reset」回到最佳化前之狀態。
7.「Open excel」打開計算結果檔案可查看詳細資訊(會存在data folder)，並檢查是否有"#NAME"錯誤。
8.「Import excel」匯入軟體生成的excel 。
9.「#NAME」excel若有”#NAME”錯誤，點擊按鈕進入server路徑，複製"XLOOKUPs.xla"至本機並依附圖設定，再按「Import excel」更新。
10.「Expore AE.cpp」匯出調教檔。
11.推入手機後拍照測試是否如預期。
12.如否回第1步。

"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)
        self.setStyleSheet(
            """
            font-family:微軟正黑體;
            font-weight: bold;
            font-size: 15pt;
            """
        )
        self.viewport().setCursor(QCursor(Qt.IBeamCursor))