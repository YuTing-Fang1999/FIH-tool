from PyQt5.QtWidgets import (
    QTabWidget, QStatusBar, QWidget, QLabel,
    QMainWindow, QMessageBox, QToolButton,
    QVBoxLayout, QScrollArea, QSplitter
)
from PyQt5.QtCore import pyqtSignal
import sys
import subprocess

class Logger(QWidget):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        VLayout = QVBoxLayout(self)
        self.info = QLabel("")
        
        #Scroll Area Properties
        scroll = QScrollArea() 
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.info)
        VLayout.addWidget(scroll)

        self.Vscroll_bar = scroll.verticalScrollBar()
        self.Vscroll_bar.rangeChanged.connect(self.scroll_range_changed_handler)
        self.Vscroll_bar.valueChanged.connect(self.scroll_value_changed_handler)
        self.scroll_falg = False
        self.auto_scroll = True

        self.signal.connect(self.show_info)

        # self.setStyleSheet(
        #     """
        #     background-color: rgb(0, 0, 0);
        #     font-size:10pt; 
        #     font-family:微軟正黑體; 
        #     color:white;
        #     """
        # )

        # if self.run_cmd("adb")!=0:
        #     self.signal.emit("可能是沒安裝adb，請先安裝adb")

    def clear_info(self):
        self.info.setText("")
        
    def show_info(self, info):
        pre_text=self.info.text()
        print(info)
        self.info.setText(pre_text+info+'\n')

        if self.auto_scroll:
            self.scroll_falg=True
            self.Vscroll_bar.setValue(self.Vscroll_bar.maximum())

    def scroll_range_changed_handler(self, minV, maxV):
        if self.scroll_falg:
            self.Vscroll_bar.setValue(maxV)
            self.scroll_falg=False

    def scroll_value_changed_handler(self, value):
        if self.Vscroll_bar.maximum()!=value:
            self.auto_scroll=False
        else: 
            self.auto_scroll=True

    def run_cmd(self, cmd, shell=False):
        """
        開啟子進程，執行對應指令，控制台打印執行過程，然後返回子進程執行的狀態碼和執行返回的數據
        :param cmd: 子進程命令
        :param shell: 是否開啟shell
        :return: 子進程狀態碼和執行結果
        """
        # self.signal.emit('************** START **************')
        # self.signal.emit(cmd)
        try:
            p = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            self.signal.emit('************** FAILED **************')
            return -1, ""
        result = []
        while p.poll() is None:
            line = p.stdout.readline().strip()
            if line:
                line = _decode_data(line)
                result.append(line)
                self.signal.emit(line)
            # 清空緩存
            sys.stdout.flush()
            sys.stderr.flush()
        # 判斷返回碼狀態
        if p.returncode == 0:
            # self.signal.emit('************** SUCCESS **************')
            pass
        else:
            self.signal.emit('************** FAILED **************')
        return p.returncode, '\r\n'.join(result)


def _decode_data(byte_data: bytes):
    """
    解碼數據
    :param byte_data: 待解碼數據
    :return: 解碼字符串
    """
    try:
        return byte_data.decode('utf-8')
    except UnicodeDecodeError:
        return byte_data.decode('GB18030')





