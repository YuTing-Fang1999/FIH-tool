# import numpy as np
# arr = np.array([0.0927, 0.5928, 0.0964, 0.8743, 0.168, 0.0212, 0.9929])
# arr[3:] /= 2
# print(arr.tolist())

from PyQt5.QtWidgets import QApplication, QTextBrowser
import markdown

app = QApplication([])

text = """
# Heading 1
This is a **bold** text.
<br><br>
## Heading 2
This is an *italic* text.

### Heading 3
This is a bullet list:
- Item 1
- Item 2
- Item 3

"""

html = markdown.markdown(text)
browser = QTextBrowser()
browser.setHtml(html)
browser.show()

app.exec_()

