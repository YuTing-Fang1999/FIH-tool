from PyQt5.QtWidgets import (
    QApplication, QMainWindow,
    QWidget, QGridLayout, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox
)
from PyQt5.QtCore import Qt
import numpy as np
import json

class ParamRangeItem(QWidget):
    def __init__(self, title, name, row):
            super().__init__()
            self.label_defult_range = []
            self.lineEdits_coustom_range = []

            VLayout = QVBoxLayout(self)

            gridLayout = QGridLayout()
            gridLayout.setContentsMargins(0, 0, 0, 0)
            gridLayout.setHorizontalSpacing(7)

            label_title = QLabel(title)
            # label_title.setStyleSheet("background-color:rgb(72, 72, 72);")

            gridLayout.addWidget(QLabel("預設範圍"), 0, 1)
            gridLayout.addWidget(QLabel("自訂範圍"), 0, 2)

            for i in range(row):
                label = QLabel()
                label.setText("#")
                self.label_defult_range.append(label)

                lineEdit = QLineEdit()
                self.lineEdits_coustom_range.append(lineEdit)

            for i in range(1, row+1):
                label_name = QLabel()
                label_name.setText(name[i-1])
                label_name.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
                gridLayout.addWidget(label_name, i, 0)

                gridLayout.addWidget(self.label_defult_range[i-1], i, 1)
                gridLayout.addWidget(self.lineEdits_coustom_range[i-1], i, 2)

            gridLayout.setColumnStretch(0, 2)
            gridLayout.setColumnStretch(1, 3)
            gridLayout.setColumnStretch(2, 3)

            VLayout.addWidget(label_title)
            VLayout.addLayout(gridLayout)


class ParamRangeBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.param_range_items = []
        self.VLayout = QVBoxLayout(self)
        self.VLayout.setContentsMargins(0, 0, 0, 0)

    def reset_UI(self):
        self.param_range_items = []
        # delete
        for i in range(self.VLayout.count()):
            self.VLayout.itemAt(i).widget().deleteLater()

    def update_UI(self, key_config):
        self.reset_UI()
        for i in range(len(key_config["title"])):
            item = ParamRangeItem(key_config["title"][i], key_config["name"][i], len(key_config["col"][i]))
            self.param_range_items.append(item)
            self.VLayout.addWidget(item)

    def update_defult_range(self, defult_range):
        idx = 0
        for item in self.param_range_items:
            for label in item.label_defult_range:
                label.setText(str(defult_range[idx]))
                idx += 1

    def update_coustom_range(self, coustom_range):
        idx = 0
        for item in self.param_range_items:
            for label in item.lineEdits_coustom_range:
                label.setText(str(coustom_range[idx]))
                idx += 1
        
    # def set_data(self):
    #     print('set ParamRangeBlock data')
    #     config = self.config[self.root][self.key]
    #     block_data = self.data[self.root][self.key]
    #     block_data["coustom_range"] = []

    #     for item in self.param_range_items:
    #         for lineEdit in item.lineEdits_range:
    #             if lineEdit.text() == "": 
    #                 return False
    #             block_data["coustom_range"].append(json.loads(lineEdit.text()))
        
    #     if len(block_data["coustom_range"]) > 0:
    #         if self.key == "ASF" or self.key == "ABF":
    #             block_data['bounds'] = [block_data['coustom_range'][0]]
    #         else: 
    #             block_data['bounds'] = [block_data['coustom_range'][0]]*block_data['lengths'][0]
                
    #         for i in range(1, len(block_data['lengths'])):
    #             if self.key == "ASF" or self.key == "ABF":
    #                 block_data['bounds'] = np.concatenate([block_data['bounds'] , [block_data['coustom_range'][i]]])
    #             else:
    #                 block_data['bounds'] = np.concatenate([block_data['bounds'] , [block_data['coustom_range'][i]]*block_data['lengths'][i]])

    #         block_data['bounds']=block_data['bounds'].tolist()

    #     return True

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setCentralWidget(ParamRangeBlock())
    MainWindow.show()
    sys.exit(app.exec_())