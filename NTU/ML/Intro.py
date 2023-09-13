from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### MLGenDataset
#### 在開始前請記得adb root 與 adb remont   
1. 選擇 c6project 或 c7project   
    * 如果是c6project  
        * 請選擇CMax資料夾   
    * 如果是c7project  
        * 請選擇c7project資料夾  
        * Load ParameterParser.exe  
        * 填入bin name(一定要填正確!)  
2. 選擇要tuning的region，在拍之前一定要將亮度調到對應的region  
3. 選擇要將生成的資料存放到哪個資料夾  
4. 點「開始拍照」按鈕即可開始產生資料集  
5. 產生的資料如下  
	* dataset dir  
    	-- param_norm.csv (標準化後的參數 50組)   
        -- param_denorm.csv (還原後的參數 50組)   
        -- 0.jpg、1.jpg、.....49.jpg (總共50張照片)     
        
### MLAlignDataset
對齊是很關鍵的一步，資料集與競品機的照片都要對齊後才能進行後續的訓練  

### MLTrain
請看TrainIntro  

### MLRecommand
請看RecommandIntro  

### MLPushAndCapture
#### 在開始前請記得adb root 與 adb remont    
img name會跟param.txt的檔名一樣   
設定好後，按開始拍攝的按鈕，就能將param.txt的參數推入手機，拍攝結果照片   
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