from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
#### 請事先使用Qualcomm DbgCfgTool apk或是MTK DebugLogger apk軟體錄製log， 而且DbgCfgTool或是DebugLogger需要紀錄到時間(例如: DbgCfgTool apk要將Log Output Format設定成threadtime)，否則此工具無法解析。   
此工具是用來從log中擷取出每張照片帶有特定關鍵字的log資訊。   
適合使用的時機: 需要連續拍攝很多張照片，並分析某幾張照片的AF對焦行為。例如: AF lab大量測試、外拍有拍攝大量照片的情況。   
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