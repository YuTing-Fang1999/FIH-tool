from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown


class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

###目的：
將測試資料依照LV及DR分類

操作：
 1.「Data folder」須包含測試機照片、測試機exif、參考機照片(檔名範例:1_SX3, 1_SX3.exif, 1_E7.jpg)。  
 2. .exif檔案需使用Debug Parser或MediaToolKit(選取ISP即可)。  
 3.「TONE.cpp」匯入相應調教檔。  
 4.「Range Settings」可調整LV、DR分類區間。  
 5.「Reset」將「Rane Settings」回復成預設值。  
 6.「Categorizer」進行分類。  
 7.「Open Folder」打開分類好的資料夾。  
 8. 打開輸出Excel在儲存格H4輸入照片編號可查表。  
 9.「Update」若Excel內容有#NAME錯誤，依照指示下載檔案及相關設定後再點擊「Update」更新Excel。  
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
