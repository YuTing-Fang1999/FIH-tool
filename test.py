from PyQt5 import QtCore, QtGui, QtWidgets
class PushButton(QtWidgets.QPushButton):
    def closeEvent(self, event):
        for children in self.findChildren(
            QtWidgets.QWidget, options=QtCore.Qt.FindDirectChildrenOnly
        ):
            children.close()
        print("closeEvent PushButton")
        super(PushButton, self).closeEvent(event)


class LineEdit(QtWidgets.QLineEdit):
    def closeEvent(self, event):
        for children in self.findChildren(
            QtWidgets.QWidget, options=QtCore.Qt.FindDirectChildrenOnly
        ):
            children.close()
        print("closeEvent LineEdit")
        super(LineEdit, self).closeEvent(event)


class ComboBox(QtWidgets.QComboBox):
    def closeEvent(self, event):
        for children in self.findChildren(
            QtWidgets.QWidget, options=QtCore.Qt.FindDirectChildrenOnly
        ):
            children.close()
        print("closeEvent ComboBox")
        super(ComboBox, self).closeEvent(event)


class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        button_close = PushButton(text="close", clicked=self.close)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(button_close)
        lay.addWidget(LineEdit())
        lay.addWidget(ComboBox())

    def closeEvent(self, event):
        for children in self.findChildren(
            QtWidgets.QWidget, options=QtCore.Qt.FindDirectChildrenOnly
        ):
            children.close()
        print("closeEvent Widget")
        super(Widget, self).closeEvent(event)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())