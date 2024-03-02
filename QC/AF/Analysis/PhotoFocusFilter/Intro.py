from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown


class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

說明:  
1.「Photo Folder」匯入同一區間照片資料夾。  
2.「Compute」計算焦點分數，CMD顯示計算過程及結果。  
3.「Open folder」打開資料夾，低於Threshold照片名稱"Fail_"。  
4.右欄顯示焦點最低分及最高分照片。  
※因使用標準差計算，"Fail_"不必然是失焦。  
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
