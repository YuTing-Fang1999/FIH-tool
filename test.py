import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTextBrowser, QVBoxLayout, QWidget

def set_cursor_position():
    # Create a PyQt application
    app = QApplication(sys.argv)

    # Create a QWidget as the main window
    window = QWidget()
    window.setWindowTitle('QTextBrowser Cursor Example')

    # Create a QTextBrowser widget
    text_browser = QTextBrowser()
    text_browser.setPlainText("This is some sample text.\nYou can set the cursor position in this text.")

    # Create a QVBoxLayout to add the QTextBrowser to the window
    layout = QVBoxLayout()
    layout.addWidget(text_browser)

    # Set the layout for the main window
    window.setLayout(layout)

    def set_ibeam_cursor(event):
        cursor_position = text_browser.cursorForPosition(event.pos())
        cursor_position.select(QTextCursor.WordUnderCursor)
        text_browser.setTextCursor(cursor_position)
        text_browser.setCursor(Qt.IBeamCursor)

    def reset_cursor():
        text_browser.unsetCursor()

    # Connect the mouse hover event to set the I-beam cursor
    text_browser.setMouseTracking(True)
    text_browser.viewport().installEventFilter(text_browser)
    text_browser.viewport().setCursor(Qt.IBeamCursor)

    # Show the window
    window.show()

    # Run the PyQt application
    sys.exit(app.exec_())

if __name__ == '__main__':
    set_cursor_position()
