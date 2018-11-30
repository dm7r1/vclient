from PySide.QtGui import *
from superdata.us3r import user

class SearchButton(QPushButton):
	def __init__(self, search_line):
		super(SearchButton, self).__init__()
		self.search_line = search_line
		self.setText("Search")
		self.setObjectName("SearchButton")

	def mousePressEvent(self, *args, **kwargs):
		if self.search_line.text() and len(self.search_line.text()) > 0:
			user.server.search_people(self.search_line.text())

