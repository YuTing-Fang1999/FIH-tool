from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目標
拍攝 step chart  
調整gamma
<br>
### 操作 
(1)輸入初始資料:  將before的參數和照片填入後點下方 ”Export data to excel & Open excel” 按鈕

(2)規劃求解:
到 excel 上執行、微調規劃求解

執行完規劃求解後回到此UI點下” Reload excel data ”按鈕刷新UI看after區塊的資料

重複步驟(2)直到調整完畢，將規劃求解後的gamma貼到code上

"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)