from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

app = QApplication([])

# Create main widget and layout
main_widget = QWidget()
main_layout = QVBoxLayout()
main_widget.setLayout(main_layout)

# Create horizontal layout for buttons
button_layout = QHBoxLayout()

# Add buttons to the layout
button1 = QPushButton('Button 1')
button2 = QPushButton('Button 2')
button3 = QPushButton('Button 3')
button_layout.addWidget(button1)
button_layout.addWidget(button2)
button_layout.addWidget(button3)

# Add the button layout to the main layout
main_layout.addLayout(button_layout)

main_widget.show()
app.exec_()
