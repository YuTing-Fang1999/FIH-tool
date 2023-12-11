from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown


class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

說明:  
1.「Photo Folder」匯入已編號成組的照片(1_E7.jpg, 1_SX3.jpg, 1_DG1.jpg)。  
2.「Keyword」輸入檔名關鍵字測試機名稱/版號(將套用其ISO值)。  
3.「Implemet」先跳出視窗確認原始檔案能夠被編輯及更動位置，Yes即會執行。  
4.「Open folder」打開資料夾查看結果。  

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
