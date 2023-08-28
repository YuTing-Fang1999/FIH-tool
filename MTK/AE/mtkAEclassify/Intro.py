from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

### 目的:  
幫照片做分類，根據不同BV, EVD, B2M, B2D, midratio, face, night scene做分類，並將照片放到對應資料夾   

### 使用說明：
1. 若過去已用此tool分類過照片，則點"選擇分類好的資料夾"按鈕選擇最大層的分類資料夾，並跳至步驟6。若無使用過，則從第2步驟開始。  
2. 使用Debug Parser輸出需要分析的照片exif檔(選取AE即可)、該圖檔以及對比機圖檔，放在同一個資料夾中  
3. 檔名規則：ex: {1_FLC.jpg, 1_FLC.jpg.exif, 1_ZF7.jpg}, {2_FLC.jpg, 2_FLC.jpg.exif, 2_ZF7.jpg},......   
4. 點 ” 選擇照片、exif 資料夾並執行分類 ” 按鈕，彈出選取視窗，選取資料所在的資料夾   
5. tool會首先分類 HS, face, night scene case，而 HS case 會依據不同 BV, EVD, Mid% 做照片分類，並在各 BV 下輸出一張平面 HS 分類結果 (x軸：EVD, y軸：Mid%)   
6. 根據想調整的參數類別選擇weighting或是THD，選擇weighting 右側則顯示 B2D, midratio 圖; 選擇THD 右側顯示 EVD, B2M 圖   
7. 選擇調整weighting時，可以進一步選擇下拉式選單濾出對應的BV, B2D, midratio區間的圖   
8. 選擇調整THD時，可以進一步選擇下拉式選單濾出對應的BV, EVD, B2M區間的圖   
9. 點"開啟對應region資料夾"按鈕時該region的資料夾會跳出  
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