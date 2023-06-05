from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QStackedWidget, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口布局
        layout = QVBoxLayout()

        # 创建 QStackedWidget
        self.stacked_widget = QStackedWidget()

        # 添加按钮和页面的对应关系
        self.button_page_mapping = {}

        # 创建按钮并连接到加载页面的槽函数
        for i in range(5):
            button = QPushButton(f"Page {i + 1}")
            button.clicked.connect(lambda checked, index=i: self.load_page(index))
            layout.addWidget(button)

            # 创建页面并添加到 QStackedWidget
            page = QWidget()
            self.stacked_widget.addWidget(page)

            # 将按钮和页面的对应关系保存起来
            self.button_page_mapping[button] = page

        # 将 QStackedWidget 添加到主窗口布局
        layout.addWidget(self.stacked_widget)

        # 创建主窗口中心部件
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # 设置主窗口中心部件
        self.setCentralWidget(central_widget)

    def load_page(self, index):
        # 通过索引获取页面
        page = self.stacked_widget.widget(index)

        # 将页面加载到 QStackedWidget 中
        self.stacked_widget.setCurrentWidget(page)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
