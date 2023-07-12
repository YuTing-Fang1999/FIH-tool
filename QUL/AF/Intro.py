from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
用來從log中擷取出每張照片帶有特定關鍵字的log資訊。  
  
適合使用的時機:需要連續拍攝很多張照片，並分析某幾張照片的AF對焦行為。例如: AF lab大量測試、外拍有拍攝大量照片  
提示: DbgCfgTool alog或是MTK DebugLogger需紀錄到時間(e.g. DbgCfgTool apk要將Log Output Format設定成threadtime)，否則工具無法解析。  

"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)