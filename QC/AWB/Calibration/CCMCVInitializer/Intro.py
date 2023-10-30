from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目的:  
評估Color difference後微調sRGB求CCM/CV  
  
### 操作:
1. 匯入參考機及測試機的Color checker照片(名稱規範A_1, A_2一組)  
2. 從平台調教檔(.xml)找到相應CCM值(9個)及Gamma值(1串)複製貼上  
3. 按下Solver計算  
4. 觀察Color summary, Color difference及模擬色塊來調整CCM/Saturation/CV  
5. 若達成權衡解Copy CCM/CV至原平台調教檔(.xml)  
6. 推入手機後拍照測試是否如預期  
7. 如否回第1步  
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