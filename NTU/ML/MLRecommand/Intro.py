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
3. 將利用之前train好的model做推薦  
4. 在ML資料夾裡開起cmd，輸入以下指令   
#### python train.py --is_recommand True --input_param_dim 16 --lr 1e-3 --outdir=target_run --run_dir region1_target --img_data=datasets/競品機資料集 --gpus 1 --kimg 3 --gamma 10 --aug noaug --metrics True --eval_img_data None --batch 16 --snap 1 --resume 模型位置


ex: 假設競品機資料集為region1_target_align、假設模型位置為training_run/region1_train/network-snapshot-000000.pkl
#### python train.py --is_recommand True --input_param_dim 16 --lr 1e-3 --outdir=target_run --run_dir region1_target --img_data=datasets/region1_target_align --gpus 1 --kimg 3 --gamma 10 --aug noaug --metrics True --eval_img_data None --batch 16 --snap 1 --resume "training_run/region1_train/network-snapshot-000000.pkl"

輸入以上指令跑完後，會將參數儲存到target_run/region1_target資料夾裡    
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