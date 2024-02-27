from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
#### 目的:
1.將log轉為.txt檔
2.擷取關鍵字log及照片對應成組

#### 操作:
1.錄製log－使用Qualcomm DbgCfgTool apk (Log Output Format設定成threadtime)，或是MTK DebugLogger apk（需記錄時間）。
2.「寫入設定檔」寫入新的設定以便下次可以直接使用相同資訊。
3.「打開設定檔資料夾」可直接編輯／刪除設定檔.json（※僅在本機端，若git pull可能會受影響）。
4.「選擇圖片資料夾」匯入圖片資料夾。
5.「選擇 log資料夾」匯入log資料夾。
6.「選擇匯出資料夾」須建立一新資料夾，不可同圖片/Log路徑。
※log原使檔轉為.txt後會被覆蓋。
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
