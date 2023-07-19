import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme

from TraditionalParamTuning.controller import MainWindow_controller as TraditionalParamTuningWidget
app = QApplication(sys.argv)
Form = TraditionalParamTuningWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())