from PySide.QtGui import *
from .searchButton import SearchButton


class SearchLine(QHBoxLayout):
	def __init__(self):
		super(SearchLine, self).__init__()
		line = QLineEdit()
		line.setPlaceholderText("Enter the username...")
		self.addWidget(QLabel("Search "))
		self.addWidget(line)
		self.addWidget(SearchButton(line))
