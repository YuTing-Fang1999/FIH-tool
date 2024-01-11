from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### GenDataset
1. 選擇 ISP Simulator Project   
2. 選擇要將生成的資料存放到哪個資料夾  
3. 點「Start」按鈕即可開始產生資料集  
4. 產生的資料如下  
	* dataset dir  
    	-- param_norm.csv (標準化後的參數 200組)   
        -- param_denorm.csv (還原後的參數 200組)   
        -- 0.jpg、1.jpg、.....199.jpg (總共200張照片)     
        -- unprocessed.jpg      
        
### AlignDataset
1. 創一個資料夾，並且將0.jpg與target.jpg放到裡面  
2. 選擇此資料夾後，按「開始對齊」按鈕即可開始對齊  
3. 最後將對齊好的target.jpg放到dataset dir中   
4. 確定資料集的資料如下    
	* dataset dir  
    	-- param_norm.csv (標準化後的參數 200組)   
        -- param_denorm.csv (還原後的參數 200組)   
        -- 0.jpg、1.jpg、.....199.jpg (總共200張照片)  
        -- unprocessed.jpg  
        -- target.jpg (競品機的照片)  

### SelectROI  
#### my_ROI.txt  
1. 選擇0.jpg  
2. 選擇ROI  
3. 在dataset dir創一個my_ROI.txt，並且將ROI的座標寫入  

#### target_ROI.txt  
1. 選擇target.jpg  
2. 選擇ROI  
3. 在dataset dir創一個target_ROI.txt，並且將ROI的座標寫入  

#### 確定資料集的資料如下    
    * dataset dir  
        -- param_norm.csv (標準化後的參數 200組)   
        -- param_denorm.csv (還原後的參數 200組)   
        -- 0.jpg、1.jpg、.....199.jpg (總共200張照片)     
        -- unprocessed.jpg      
        -- target.jpg (競品機的照片)  
        -- my_ROI.txt  
        -- target_ROI.txt  

### Train
請看TrainIntro  

### Recommand
請看RecommandIntro  

### PushParam
設定好後，按Start的按鈕，就能將param.txt的參數推入手機，得到結果照片   
img name會跟param.txt的檔名一樣   
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