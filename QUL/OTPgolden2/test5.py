import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication(sys.argv)

file_dialog = QFileDialog()
file_dialog.setAcceptMode(QFileDialog.AcceptSave)
file_dialog.setNameFilter("All Files (*);;Text Files (*.txt)")
file_dialog.setDirectory("./")
file_dialog.exec_()

selected_files = file_dialog.selectedFiles()
if selected_files:
    selected_file = selected_files[0]
    print('Selected file:', selected_file)

sys.exit(app.exec_())
