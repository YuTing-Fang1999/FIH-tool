from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
直接裁剪成相同大小: 是以左上角為原點剪裁  
resize成相同大小: 是等比例縮放後，再以左上角為原點剪裁  
目的是為了讓長寬一樣  
  
如果以視覺來說，照片的範圍一樣但解析度不同的話，比較推薦用resize的  
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