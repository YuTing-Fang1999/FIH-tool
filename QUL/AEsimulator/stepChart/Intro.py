from PyQt5.QtWidgets import QTextEdit, QLabel

class Intro(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        # self.setMarkdown("""
        # ### Hello  *World*~~!~~ 
        # ### 13
        # """)
        self.setMarkdown(
"""
### 目標
拍攝 step chart 
調整gamma 
\n\n\n\n\




### 操作\n
(1) 輸入初始資料:  將before的參數和照片填入後點下方 ”Export data to excel & Open excel” 按鈕\n

(2) 規劃求解:\n
到 excel 上執行、微調規劃求解\n
執行完規劃求解後回到此UI點下” Reload excel data ”按鈕刷新UI看after區塊的資料\n
重複步驟(2)直到調整完畢，將規劃求解後的gamma貼到code上\n
"""
        )