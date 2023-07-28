import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor

class ExampleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Item Background Example")
        self.setGeometry(100, 100, 500, 300)

        # Create a QTableWidget
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        # Fill the table with some data for demonstration purposes
        for row in range(5):
            for col in range(3):
                self.tableWidget.setItem(row, col, QTableWidgetItem(f"Row {row}, Col {col}"))

                # Set the background color of the individual item
            self.tableWidget.item(row, 1).setBackground(QColor(255, 255, 0))  # Yellow background

        # Set the table as the central widget
        central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.tableWidget)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec_())
