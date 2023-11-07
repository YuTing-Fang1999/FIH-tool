
---------------------------------------------------------------------------

18.mtkclassifyTONEanalysis
分為18.mtkclassifyTONEanalysis_SX3.py, 18.mtkTONEanalysis_SX3.py兩種，差別是有無事先分類
使用說明：

	1. 使用Debug Parserc或MediaToolKit輸出需要分析的照片exif檔(選取ISP即可)、該圖檔以及對比機圖檔，放在同一個資料夾中
	2. 檔名規則：ex: {1_FLC.jpg, 1_FLC.jpg.exif, 1_ZF7.jpg}, {2_FLC.jpg, 2_FLC.jpg.exif, 2_ZF7.jpg},......
	3. 將三個檔案一組的資料放入Exif資料夾中，可以一次放入多組，結果會分別填入表格列中，每20組存一個excel檔，防止檔案過大
	4. run py檔，可選擇是否要事先分類
	5. 彈出選取視窗，選取照片拍攝時使用的TONE.cpp檔
	6. 鍵入0代表無對比機照片，鍵入1代表有對比機照片
	7-1. 若選擇先分類，會將分類結果分別產生成mtkTONEanalysis_yy_mm_dd_ss_LVregion_DRregion.xlsx
	7-2. 若不事先分類，會產生mtkTONEanalysis_yy_mm_dd_ss_startNum_endNum.xlsx

----------------------------------------------------------------------------

2023.06.29 First release
2023.08.07 18.mtkTONEanalysis_SX3.py的print詞修改