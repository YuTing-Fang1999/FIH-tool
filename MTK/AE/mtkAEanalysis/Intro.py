from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

### 使用說明：
1. mtkAEclassify.exe處理完後，選擇要分析的照片區間，並將三個檔案一組的資料放入Exif資料夾中   
2. 可以一次放入多組，結果會分別產生在不同Sheet中，每20組存一個excel檔，防止檔案過大   
3. 選擇專案   
4. 點”選擇照片、exif 資料夾”按鈕，選擇放置照片與exif的資料夾   
5. 點”選擇code”按鈕，選取照片拍攝時使用的AE.cpp檔   
6. 選完會自動產生mtkAEanalysis_yy_mm_dd_ss_startNum_endNum.xlsx   
7. 由於每20組照片產生一個excel，若照片組數數量超過20會產生多個excel，點下拉式選單選擇要顯示的excel  
8. 點 ”開啟excel” 按鈕，便可以檢視分析結果的 excel，若要開啟其餘 excel，便重複步驟7、步驟8  
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