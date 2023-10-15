from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
#### 
1. 請選擇資料夾路徑
2. 點「Start」按鈕即可開始產生資料集  
3. 產生的資料如下  
	* dataset dir  
    	-- param_norm.csv (標準化後的參數 50組)   
        -- param_denorm.csv (還原後的參數 50組)   
        -- 0.jpg、1.jpg、.....49.jpg (總共50張照片)     
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