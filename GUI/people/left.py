from PySide.QtGui import QStackedLayout, QFrame, QVBoxLayout
from .panel import Block
from .personImpl import Contact, SearchedPerson, Request
from GUI.inCalls import InCallsLayout
from superdata.us3r import user


class LeftContainer(QFrame):
	def __init__(self):
		super(LeftContainer, self).__init__()
		self.setFixedWidth(260)

		self.stacked_layout = QStackedLayout()
		self.contacts = Block(Contact, "Contacts", user.get_contacts())
		self.requests = Block(Request, "Requests", user.get_requests())

		def search_func(text):
			user.server.search_people(text)

		self.people = Block(SearchedPerson, "Global search", [], search_func)

		self.stacked_layout.addWidget(self.contacts)
		self.stacked_layout.addWidget(self.requests)
		self.stacked_layout.addWidget(self.people)

		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		layout.setSpacing(0)
		layout.addLayout(self.stacked_layout)
		self.setLayout(layout)

		self.in_calls_layout = InCallsLayout()
		self.in_calls_layout.setParent(self)
		self.in_calls_layout.move(400, 20)
		self.in_calls_layout.setFixedHeight(0)
		layout.addWidget(self.in_calls_layout)

		self.show_contacts()

	def show_contacts(self):
		self.stacked_layout.setCurrentIndex(0)

	def show_requests(self):
		self.stacked_layout.setCurrentIndex(1)

	def show_people(self):
		self.stacked_layout.setCurrentIndex(2)


