from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目的: 求 luma target   
### 操作說明:  
1.拍攝24色卡  
2.將 code 中初始 default gamma 填入 Gamma from C7   
3.點"Load Ours"按鈕選擇tuning手機照片、點"Load Ref"按鈕選擇參考機照片  
4.將 C7 上的 luma target 填入  
5.按"Compute"按鈕，並將計算出的luma target填回C7  
6.若有需要可以點"Open Excel"按鈕，查看詳細excel內容  
"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)