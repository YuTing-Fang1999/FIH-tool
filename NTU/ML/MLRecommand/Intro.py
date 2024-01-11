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
3. 在ML資料夾裡開起cmd，輸入以下指令   

set dataset_name="07"  
python train.py --is_recommand True ^  
--resume training_run/%dataset_name%/Model.pkl ^  
--dataset_paths=datasets/%dataset_name% ^  
--outdir=target_run/%dataset_name% ^  
--input_param_dims 19 ^  
--resolution 256 --lr 1e-3 --gpus 1 --batch 16 --snap 5 --kimg 10   

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