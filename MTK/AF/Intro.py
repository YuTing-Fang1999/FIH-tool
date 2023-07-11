from PyQt5.QtWidgets import QTextBrowser
import markdown

class Intro(QTextBrowser):
    def __init__(self):
        super().__init__()
        markdown_content = """
### AF
"""
        html = markdown.markdown(markdown_content)
        self.setHtml(html)