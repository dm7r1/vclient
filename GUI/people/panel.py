from PySide.QtGui import QFrame, QVBoxLayout, QScrollArea, QSizePolicy, QLineEdit, QLabel
from PySide.QtCore import QEvent, Qt
from superdata.us3r import user


class Panel(QFrame):
	def __init__(self, PersonClassImpl, people):
		super(Panel, self).__init__()
		self.setObjectName("PeoplePanel")
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(2)
		self.setLayout(self.layout)
		self.PersonClassImpl = PersonClassImpl
		self.setFixedWidth(260)
		self.people = people
		self.update_people()

	def update_people(self):
		while 1:
			widget = self.layout.takeAt(0)
			if not widget:
				break
			self.layout.removeItem(widget)

		for person in self.people:
			person = self.PersonClassImpl(person)
			self.layout.addWidget(person)

		self.setFixedHeight(len(self.people) * 56 + 2)
		self.layout.addStretch()

	def event(self, event):
		if event.type() == 666:
			self.update_people()
		return super(Panel, self).event(event)


class Block(QFrame):
	def __init__(self, PersonClassImpl, label_text, people, search=False):
		super(Block, self).__init__()
		self.setFixedWidth(260)
		self.setObjectName("Left")
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(5, 0, 0, 0)
		label = QLabel(label_text)
		label.setFixedHeight(36)
		label.setAlignment(Qt.AlignCenter)
		label.setObjectName("LeftBlockLabel")
		self.layout.addWidget(label)
		if search:
			class SearchLine(QLineEdit):
				def __init__(self):
					super(SearchLine, self).__init__()
					self.setPlaceholderText("Search")
					self.setObjectName("PeopleSearchLine")

				def keyPressEvent(self, event):
					if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and len(self.text()) > 0:
						search(self.text())
					super(SearchLine, self).keyPressEvent(event)

			edit_line = SearchLine()

			self.layout.addWidget(edit_line)
		self.panel = Panel(PersonClassImpl, people)
		scroll_area = QScrollArea()
		scroll_area.setObjectName("LeftScrollArea")
		scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll_area.setWidget(self.panel)
		self.layout.addWidget(scroll_area)
		self.setLayout(self.layout)
		scroll_area.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored))

	def post_event_update(self):
		user.qtapp.postEvent(self.panel, QEvent(QEvent.Type(666)))

	def showIt(self):
		self.setVisible(True)
		self.panel.update_people()

	def set_people(self, people):
		self.panel.people = people
