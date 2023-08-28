from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目標: 
拍攝 step chart 並調整 gamma   

### 操作: 
(1)輸入初始資料:   
   按"load gamma15.xml"按鈕，選擇tuning前的gamma15.xml(只能load gamma15.xml)code，並按 "load ref photo"、"load ori photo"選參考機的照片與調整前的照片後，點上方"Export data to excel & Open excel" 按鈕，會自動算出step chart亮度  

(2)規劃求解:   
   到 excel 上執行、微調規劃求解  
   執行完規劃求解後回到此UI點下 "Reload excel data" 按鈕刷新UI看after區塊的資料  
   
(3)重複步驟(2)直到調整完畢，將規劃求解後的gamma貼到code上  

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