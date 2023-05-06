import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QButtonGroup

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        # Create vertical layout
        vbox = QVBoxLayout(self)
        
        # Create button group
        self.group = QButtonGroup()
        
        # Create buttons and add them to the group
        self.button1 = QPushButton('Button 1', self)
        self.button1.setCheckable(True)
        self.group.addButton(self.button1)
        vbox.addWidget(self.button1)
        
        self.button2 = QPushButton('Button 2', self)
        self.button2.setCheckable(True)
        self.group.addButton(self.button2)
        vbox.addWidget(self.button2)
        
        self.button3 = QPushButton('Button 3', self)
        self.button3.setCheckable(True)
        self.group.addButton(self.button3)
        vbox.addWidget(self.button3)
        
        # Set the button group to be exclusive
        self.group.setExclusive(True)
        
        # Connect the button group to a function that prints the selected button's text
        # self.group.buttonClicked.connect(self.buttonClicked)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QPushButton Example')
        self.show()
    
    def buttonClicked(self, button):
        print('Selected button:', button.text())

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
