import sys
from PyQt5.QtWidgets import QFileDialog, QLabel, QHBoxLayout, QPushButton, QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import Qt, QMimeData
from myPackage.ParentWidget import ParentWidget

class MyWidget(ParentWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XML Viewer")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a QHBoxLayout for loading xml
        load_layout = QHBoxLayout()
        self.load_button = QPushButton('load xml')
        self.load_button.clicked.connect(self.load_xml)
        self.path_label = QLabel(self)
        load_layout.addWidget(self.load_button)
        load_layout.addWidget(self.path_label)
        load_layout.setStretch(0,0)
        load_layout.setStretch(1,1)

        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["Element", "Value"])
        self.tree_widget.itemClicked.connect(self.item_clicked)
        self.tree_widget.setColumnWidth(0, 900)  # Width of the first column

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search...")
        self.search_input.textChanged.connect(self.search_xml)
        
        # Create a QHBoxLayout for copying text
        path_layout = QHBoxLayout()
        self.text_label = QLabel(self)
        self.text_label.setText("XML Path: ")
        self.text_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.copy_button = QPushButton('Copy')
        self.copy_button.clicked.connect(self.copy_text)
        path_layout.addWidget(self.text_label)
        path_layout.addWidget(self.copy_button)
        path_layout.setStretch(0,1)
        path_layout.setStretch(1,0)

        self.central_layout = QVBoxLayout(self)
        self.central_layout.addLayout(load_layout)
        self.central_layout.addWidget(self.search_input)
        self.central_layout.addLayout(path_layout)
        self.central_layout.addWidget(self.tree_widget)

        self.xml_doc = None  # Store the XML document for reusing during search
        self.root_element = None  # Store the root element for reusing during search
        
        if self.get_path("ML_config_setting_xml_path") != "./":
            self.path_label.setText(self.get_path("ML_config_setting_xml_path"))
            self.load_xml(self.get_path("ML_config_setting_xml_path"))

    def load_xml_path(self):
        filepath, filetype = QFileDialog.getOpenFileName(self,"Please choose xml file", self.get_path("ML_config_setting_xml_path"), 'Code Files(*.xml)')

        if filepath == '':
            return
        self.set_path("ML_config_setting_xml_path", filepath)
        self.path_label.setText(filepath)
        self.load_xml(filepath)
        
    def load_xml(self, filepath):
        self.xml_doc = QDomDocument()
        file = open(filepath, 'r')
        self.xml_doc.setContent(file.read())
        file.close()

        self.root_element = self.xml_doc.documentElement()
        self.populate_tree(self.tree_widget, self.root_element)
        self.tree_widget.expandAll()

    def populate_tree(self, tree_item, xml_node):
        if xml_node.isElement():
            item = QTreeWidgetItem(tree_item, [xml_node.toElement().tagName()])

            child_nodes = xml_node.childNodes()
            if child_nodes.count() == 1 and child_nodes.item(0).toElement().tagName() == "":
                item.setText(1, xml_node.toElement().text())
            else:
                for i in range(child_nodes.count()):
                    child_node = child_nodes.item(i)
                    self.populate_tree(item, child_node)

    def search_xml(self):
        search_query = self.search_input.text().lower()
        if search_query.strip() != "":  # If the search field is empty
            self.clear_tree(self.tree_widget.invisibleRootItem())
            self.search_in_tree(self.tree_widget.invisibleRootItem(), search_query)
            self.tree_widget.expandAll()
        else:
            self.show_tree(self.tree_widget.invisibleRootItem())

    def search_in_tree(self, tree_item, search_query):
        can_search = False
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            if self.search_in_tree(child_item, search_query):
                tree_item.setHidden(False)
                can_search = True
        
        if tree_item.childCount() == 0:
            tree_item.setHidden(False)
            
        if search_query in tree_item.text(0).lower():
            return True
            
        return can_search
    
    def clear_tree(self, tree_item):
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            child_item.setHidden(True)
            self.clear_tree(child_item)
            
    def show_tree(self, tree_item):
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            child_item.setHidden(False)
            self.show_tree(child_item)

    def item_clicked(self, item, column):
        if item.text(1) == "":
            self.text_label.setText("Please select a node with parameters.")
            return
        xml_path = self.get_xml_path(item)
        self.text_label.setText(str(xml_path))
        print("XML Path:", xml_path)

    def get_xml_path(self, item):
        def item_index(item):
            if item.parent():
                tag_name = item.text(0)
                count = 0
                for i in range(item.parent().indexOfChild(item)):
                    sibling = item.parent().child(i)
                    if sibling.text(0) == tag_name:
                        count += 1
                return count
            return 0
                
        path_list = []
        parent_item = item

        while parent_item is not None:
            path_list.insert(0, parent_item.text(0))
            path_list.insert(1, item_index(parent_item))
            parent_item = parent_item.parent()

        return path_list

    def copy_text(self):
        # Copy the text from the QLabel to the clipboard
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(self.text_label.text())
        clipboard.setMimeData(mime_data)
        
    
        

def main():
    app = QApplication(sys.argv)
    viewer = MyWidget()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
