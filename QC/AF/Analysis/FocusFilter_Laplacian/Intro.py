from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown


class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

說明:  
1.「Photo Folder」匯入同一區間照片的資料夾。  
2.「Clearest Image」計算出最高焦點分數，CMD顯示計算結果，並顯示ROI Image。  
3.「Add Blur」拉桿對最清晰照片增加高斯模糊，直至可接受的最低清晰程度，同時計算模糊下的焦點分數當threshold。  
4.「Compute」計算焦點分數，CMD顯示計算過程及結果。  
5. 重新命名原則為: 名次_分數_原檔名，分數低於Threshold照片名稱"Fail_"。  
6.「Open folder」打開資料夾。  
7.右欄顯示焦點低於threshold最高分及最高分照片。  
※因使用人眼判別，"Fail_"必然是失焦。  
※若照片失焦數量過多可能不適用。  
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
