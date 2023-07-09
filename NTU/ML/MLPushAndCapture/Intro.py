from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
請先   
abd root   
adb remount   
img name會跟param.txt的檔名一樣
設定好後，按開始拍攝的按鈕，就能將param.txt的參數推入手機，拍攝結果照片 
"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)