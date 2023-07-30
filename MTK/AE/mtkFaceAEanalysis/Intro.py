from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
1. 將 exif、參考機照片、tuning 手機照片放入同一資料夾內  
2. 點”Load exif、照片資料夾“按鈕選擇放置 exif、參考機照片、tuning 手機照片  
3. 點”load code”選擇AE.cpp  
4. 勾選不要列入計算的照片，點”刪除勾選的照片”按鈕將照片和對應資料刪除  
5. 按下最佳化按鈕  
6. 觀察THD diff是否足夠小  
7. 若不滿意可微調face link target(normal light)、 face link target(low light)  
8. 如果需要想將參數回復到最初狀態點”歸零”按鈕  
9. 調整完畢點”export code”按鈕，選擇儲存AE.cpp位置  
"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)