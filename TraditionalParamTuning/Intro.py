from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
* Step 1: 取得調試專案與推參數所需的檔案  
	* C6: CMax + tuning參數包  
	* C7: tuning參數包 + ParameterParser.exe  

* Step 2: 選擇project設定C6或是C7專案  
	* 2-1. C6專案請指定CMax資料夾，並放置參數到CMax/src資料夾內  
	* 2-2. C7專案請指定tuning參數包與ParameterParser.exe檔，並填寫推入手機的bin檔名稱(xxx.bin)  
* Step 3: 設定環境  
	* 3-1. 找一個要做NR調參的實驗場景，該場景需同時包含平坦區與細節區，並設定好環境亮度。  
	* 3-2. 首先使用調試手機拍攝該場景下的照片，並確認當前亮度是否為我們要調試的gain值區間。  
	* 3-3. 嘗試調整光源，直到達到我們要調試的gain值。  
* Step 4: 拍攝參考機的照片  
	* FOV儘可能與待測機FOV對齊，否則容易影響tool算分。  
* Step 5: 設定要框選的ROI  
	* 5-1. 將調試手機放回原處，FOV與Step 4參考機拍攝的照片FOV對齊。  
	* 5-2. 切換至「ROI設定」頁籤，接著按下「拍攝照片」。拍攝的照片會顯示在預覽框中，作為before的照片。  
* Step 6: 讀入目標照片  
	* 6-1. 目標照片是作為我們期望調試手機的NR表現想要達到的最終效果，也就是Step 4所拍攝的參考機照片。亦可根據優化需求更換其他的目標照片。  
* Step 7: 增加ROI區域  
	* 7-1. 按下「增加ROI區域」，會顯示兩張圖。左圖: 待測機照片；右圖: Step 6的目標照片  
	* 7-2. 根據要模擬的圖片區塊做框選，兩者ROI儘可能大小一致。框選ROI建議: 若使用感知距離做算分，可以同時框平坦區跟高頻區；或是框選2個ROI，其一為平坦區、另一個是細節區。  
* Step 8: 選擇量化指標  
	* 8-1. 選擇要追目標照片的量化指標，建議使用perceptual distance即可。  
* Step 9: 設定要調試的參數  
	* 9-1. 切換到「參數設定」頁籤，進行以下設定:  
        * a. 選擇要調試的ISP模塊(建議仿照正常調試順序，先做WNR，再做ASF)  
        * b. 選擇欲調試的gain值區間  
        * c. 勾選要做迭代的參數(用來標記是否要納入global/ local search的輸入參數)  
        * d.自訂範圍: 定義global/ local search推薦參數的數值範圍(可根據目前參數的表現，設定理想的參數範圍)  
        * e.設定超參數:  
		    - global search / local search: 都是用來找最佳參數的兩種演算法。前者建議在1x gain使用；後者可以用來做微調參數使用  
			- capture num: 每次計算分數時要拍幾張  
			- population size:要推幾組參數。建議數量是設定大於5，但不要超過10。  
			- generaions: 要跑幾輪。每一輪都是完整迭代population size的數量  
* Step 10: 執行參數推薦程序  
	* 10-1. 切換到「執行」標籤，按下「Run」  
	* 10-2. 點擊「Param」按鈕，會即時顯示每個參數的更新狀態  
* Step 11: 取得參數推薦結果  
	* 11-1. 待Step 10完成後，在資料夾內找到「Result_日期」資料夾，裡面會有以下內容:  
		* a.4張score最低的.jpg照片  
		* b.result.csv : 紀錄4張照片的訓練結果  
		* c.參考機照片  
		* d.框選的ROI  
* Step 12: 挑選效果最佳的照片  
	* result.csv已經由上而下排序好分數高低，越上面的代表越好。(1.jpg > 2.jpg > 3.jpg > 4.jpg)  
* Step 13: 回填參數至專案  
	* 打開result.csv，比對Step 12挑選出來的理想照片所對應的參數，將參數回填至「參數設定」->「使用文本框輸入參數」，按下「寫入」。  
* Step 14: 訓練其他模塊  
	* 若調試未完成，可以接著以同樣手法重複Step 9~Step 13訓練其它模塊。  
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