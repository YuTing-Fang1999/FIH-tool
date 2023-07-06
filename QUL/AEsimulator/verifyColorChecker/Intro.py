from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### 目的: 驗證 luma target   
### 操作說明:  
1.拍攝24色卡  
2.點"Load Ours"按鈕選擇tuning手機照片、點"Load Ref"按鈕選擇參考機照片  
3.按“Compute”按鈕，觀察diff欄位顯示的亮度差值  
4.若diff欄位顯示的亮度差值過大，須回到上一個模塊colorChcker(求luma target)重新操作一次  
5.若有需要可以點"Open Excel"按鈕，查看詳細excel內容  

"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)