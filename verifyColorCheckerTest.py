import sys
from PyQt5.QtWidgets import QApplication
import qdarktheme

from QUL.AEsimulator.verifyColorChecker.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
qdarktheme.setup_theme()
sys.exit(app.exec_())