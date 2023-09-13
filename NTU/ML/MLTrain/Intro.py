from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
1. 請使用4090那台電腦    
2. 打開桌面的ML資料夾   
3. 請先將資料集放到datasets資料夾裡   
將競品機
4. 在ML資料夾裡開起cmd，輸入以下指令   
#### python train.py --is_recommand False --input_param_dim 16 --lr 1e-3 --outdir=training_run --run_dir 要儲存的資料夾名稱 --img_data=datasets/資料集名稱 --gpus 1 --kimg 50 --gamma 10 --aug noaug --metrics True --eval_img_data None --batch 16 --snap 1 --resume "places.pkl"

ex: 假設資料集名稱為region1_align   
#### python train.py --is_recommand False --input_param_dim 16 --lr 1e-3 --outdir=training_run --run_dir region1_train --img_data=datasets/region1_align --gpus 1 --kimg 50 --gamma 10 --aug noaug --metrics True --eval_img_data None --batch 16 --snap 1 --resume "places.pkl"
輸入以上指令跑完後，會將模型儲存到training_run/region1_train資料夾裡    
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