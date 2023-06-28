from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """

### 目的:  
使用LSC Golden sample 裝在手機上容易單邊傾斜, 觀察四個LSC Calibration Gain 是否對稱是預防單邊傾斜  
確認邊緣亮度補償程度、觀察LSC補償過後圖形是否均勻且平整  
<br>
### 操作:  
1. 點"Load LSC golden OTP txt"按鈕選擇廠商給的golden OTP txt
2. 點"Export LSC golden OTP txt"按鈕選擇轉置C7直行的形式的golden OTP txt的儲存位置，並去 C7 >> LSC >> golden module >> import 選txt，做各region 的 LSC 補償優化
3. 點"Load lsc .xml"按鈕選擇lsc.xml 檔案 load 入整合 tool
4. 點下拉式選單選擇想看的region資料
5. 點" Open LSC excel"按鈕如果想看更詳細的資料再開啟 excel 檢查平坦度


"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)