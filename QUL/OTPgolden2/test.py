import sys
import os
# from qdarkstyle import load_stylesheet_pyqt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
 
class TableModelView(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data
 
    def rowCount(self, parent=None):
        return self._data.shape[0]
 
    def columnCount(self, parent=None):
        return self._data.shape[1]
 
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
 
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
 
 
class DataGroupSum(QWidget):
    def __init__(self):
        super(DataGroupSum, self).__init__()
        self.cwd = os.getcwd()
        self.init_ui()
 
    def init_ui(self):
        # 标题、图标设置
        self.setWindowTitle('Excel data lab')
 
 
        # 初始化水平布局
        hbox = QHBoxLayout()
 
        # 初始化栅格布局
        grid = QGridLayout()
 
        self.data_source_text = QLineEdit()
        self.data_source_text.setReadOnly(True)
 
        self.data_source_btn = QPushButton()
        self.data_source_btn.setText('data')
        self.data_source_btn.clicked.connect(self.data_source_btn_click)
 
        self.data_group_column = QLabel()
        self.data_group_column.setText('setlab')
 
        self.data_group_column_text = QLineEdit()
        self.data_group_column_text.setPlaceholderText('line1,line2...')
 
        self.save_dir_text = QLineEdit()
        self.save_dir_text.setReadOnly(True)
 
        self.save_dir_btn = QPushButton()
        self.save_dir_btn.setText('road')
        self.save_dir_btn.clicked.connect(self.save_dir_btn_click)
 
        self.view_data_btn = QPushButton()
        self.view_data_btn.setText('preview')
        self.view_data_btn.clicked.connect(self.view_data_btn_click)
 
        self.save_data_btn = QPushButton()
        self.save_data_btn.setText('save')
        self.save_data_btn.clicked.connect(self.save_data_btn_click)
 
        grid.addWidget(self.data_source_text, 0, 0, 1, 2)
        grid.addWidget(self.data_source_btn, 0, 2, 1, 1)
        grid.addWidget(self.data_group_column, 1, 0, 1, 1)
        grid.addWidget(self.data_group_column_text, 1, 1, 1, 2)
 
        grid.addWidget(self.save_dir_text, 2, 0, 1, 2)
        grid.addWidget(self.save_dir_btn, 2, 2, 1, 1)
        grid.addWidget(self.view_data_btn, 3, 0, 1, 2)
        grid.addWidget(self.save_data_btn, 3, 2, 1, 1)
 
        self.table_view = QTableView()
        self.table_view.setFixedWidth(500)
        self.table_view.setFixedHeight(400)
 
        hbox.addWidget(self.table_view)
        hbox.addLayout(grid)
 
        self.setLayout(hbox)
 
    def data_source_btn_click(self):
        xlsx_file = QFileDialog.getOpenFileName(self, 'choosetxt', self.cwd, 'Excel File(*.xlsx)')
        self.data_source_text.setText(xlsx_file[0])
        self.data_frame = pd.read_excel(self.data_source_text.text().strip())
        print(self.data_frame)
        model = TableModelView(self.data_frame)
        self.table_view.setModel(model)
 
    def save_dir_btn_click(self):
        save_path = QFileDialog.getExistingDirectory(self, 'chooselab', self.cwd)
        self.save_dir_text.setText(save_path + '/')
 
    def view_data_btn_click(self):
        columns = self.data_group_column_text.text().strip()
        column_list = []
        if columns != '':
            column_list = columns.split(',')
        self.data_frame_group = self.data_frame.groupby(column_list, as_index=False).sum()
        print(self.data_frame_group)
        model = TableModelView(self.data_frame_group)
        self.table_view.setModel(model)
 
    def save_data_btn_click(self):
        dir = self.save_dir_text.text().strip()
        self.data_frame_group.to_excel(dir + 'output.xlsx',sheet_name='datasum')
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
 
    # app.setStyleSheet(load_stylesheet_pyqt5())
    main = DataGroupSum()
    main.show()
    sys.exit(app.exec_())
 