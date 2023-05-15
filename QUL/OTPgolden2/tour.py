from PyQt5.QtWidgets import QApplication, QWizard, QWizardPage, QLabel, QPushButton, QVBoxLayout


class GuidedTourPage(QWizardPage):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setTitle('Guided Tour')
        self.setSubTitle(text)
        label = QLabel(text)
        button = QPushButton('Next', self)
        button.clicked.connect(self.completeChanged)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)


class GuidedTour(QWizard):
    def __init__(self):
        super().__init__()
        self.addPage(GuidedTourPage('Step 1: Click the "File" menu.'))
        self.addPage(GuidedTourPage('Step 2: Select "New" from the menu.'))
        self.addPage(GuidedTourPage('Step 3: Enter a filename and click "Save".'))
        self.setWindowTitle('Guided Tour')
        self.setWizardStyle(QWizard.ModernStyle)


if __name__ == '__main__':
    app = QApplication([])
    tour = GuidedTour()
    tour.show()
    app.exec_()
