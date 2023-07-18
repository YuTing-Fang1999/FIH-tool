import sys
from PyQt5.QtWidgets import QApplication

from MTK.AE.mtkFaceAEanalysis.MyWidget import MyWidget
app = QApplication(sys.argv)
Form = MyWidget()
Form.show()
sys.exit(app.exec_())