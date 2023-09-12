from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
1. 將 exif、參考機照片、tuning 手機照片放入同一資料夾內  
2. 點”load code”選擇AE.cpp  
3. 點”Load exif、照片資料夾“按鈕選擇放置 exif、參考機照片、tuning 手機照片  
4. 若下方照片資訊從Before Day欄位開始至最右側的Target_TH欄位的數值出現異常(例如: 數值大小異常，正常數值大小是數百左右)，一般是受office版本影響，需修改excel中XLOOKUP公式的部分參考解法:下載XLOOKUPs.xla，點”open excel”按鈕，excel 檔案>選項>進階，在一般欄位的”啟動時，開啟所有檔案於”輸入XLOOKUPs.xla所在的資料夾位置，並將excel內所有_xlfn.XLOOKUP公式替換成XLOOKUPs，公式修改後檢查excel數值顯示是否恢復正常，若仍舊異常表示excel可能有額外讀取其他檔案，必須要去一般資料夾開啟excel，讓excel重新讀取，若excel數值顯示正常，就儲存並關閉excel，點”load excel”按鈕刷新整合tool介面資訊  
5. 勾選不要列入計算的照片，點”刪除勾選的照片”按鈕將照片和對應資料刪除  
6. 按下”最佳化”按鈕  
7. 觀察THD diff是否足夠小  
8. 若不滿意可多按幾次”最佳化”按鈕或是手動微調face link target(normal light)、 face link target(low light)  
9. 如果需要想將參數回復到最初狀態點”歸零”按鈕  
10. 調整完畢點”export code”按鈕，選擇儲存AE.cpp位置  

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
        self.viewport().setCursor(QCursor(Qt.IBeamCursor))