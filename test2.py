from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QVBoxLayout, QPushButton, QStyledItemDelegate, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    tab = QTableView()
    sti = QStandardItemModel()
    sti.appendRow([QStandardItem(str(i)) for i in range(4)])
    tab.setModel(sti)
    tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
    tab.setIndexWidget(sti.index(0, 3), QPushButton("button"))
    tab.show()
    sys.exit(app.exec_())
