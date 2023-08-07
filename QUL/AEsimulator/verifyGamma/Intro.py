from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目標
拍攝 step chart  
復驗gamma  

### 操作   
(1) 選擇參考機與復驗照片  

(2) 點選 compute 檢查拍攝出的亮度差  

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