from .person import Person
from PySide.QtGui import QLabel
from PySide.QtCore import QTimer
from ..guiStates import GUIStates
from ..buttons import AddButton
from superdata.us3r import user
from datetime import datetime


class Contact(Person):
	def __init__(self, person):
		super(Contact, self).__init__(person[1])
		online = person[2][1] != -1
		self.uid = person[0]
		self.last_seen_t = person[3]
		self.status = QLabel()
		self.timer = QTimer()
		if online:
			self.status.setText("online")
		else:
			self.update_last_seen()
		self.status.setObjectName("StatusOn" if online else "StatusOff")
		self.status.setFixedHeight(24)
		self.left.addWidget(self.status)
		self.timer.timeout.connect(self.update_last_seen)

	def update_last_seen(self):
		wait, s = self.offline_time_str()
		self.status.setText(s)
		if wait != -1:
			self.timer.start(wait * 1000)

	def mousePressEvent(self, *args, **kwargs):
		GUIStates.set_contact_id(self.uid)

	def offline_time_str(self):
		last_seen = datetime.fromtimestamp(self.last_seen_t)
		now = datetime.now()
		dt = now - last_seen
		seconds_ago, minutes_ago, hours_ago, days_ago = dt.seconds, dt.seconds // 60, dt.seconds // 60 // 60, dt.days
		if days_ago == 0:
			if hours_ago == 0:
				if minutes_ago == 0:
					return 4, Contact.ago_str(seconds_ago, "second")
				return 120, Contact.ago_str(minutes_ago, "minute")
			return 3600, Contact.ago_str(hours_ago, "hour")
		if days_ago < 16:
			return 24 * 3600, Contact.ago_str(days_ago, "day")
		return -1, "last seen " + last_seen.strftime("%Y %b %d")

	@staticmethod
	def ago_str(count, item):
		return "last seen " + Contact.items_str(count, item) + " ago"

	@staticmethod
	def items_str(count, item):
		return str(count) + " " + item if count == 1 else str(count) + " " + item + "s"

class SearchedPerson(Person):
	def __init__(self, person):
		super(SearchedPerson, self).__init__(person[1])

		def send_req():
			user.server.send_request(person[0])

		self.sendButton = AddButton(send_req)
		self.main.addWidget(self.sendButton)


class Request(Person):
	def __init__(self, person):
		super(Request, self).__init__(person[1])

		def accept_req():
			user.server.add_to_contacts(person[0])

		self.acceptButton = AddButton(accept_req)
		self.main.addWidget(self.acceptButton)
