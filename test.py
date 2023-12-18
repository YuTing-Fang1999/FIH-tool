import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme

from NTU.perceptual_distance.controller import MainWindow_controller
app = QApplication(sys.argv)
Form = MainWindow_controller()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())