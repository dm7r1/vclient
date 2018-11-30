from PySide.QtGui import *
from PySide.QtCore import Qt
from superdata.us3r import user


class SendReqButton(QPushButton):
	def __init__(self, uid, req_widget, box):
		super(SendReqButton, self).__init__("Send request")
		self.setObjectName("SendReqButton")
		self.setStyleSheet("#SendReqButton{background: #476;}")
		self.setFixedWidth(120)
		self.uid = uid
		self.req_widget = req_widget
		self.box = box
		self.clicked_ = False

	def mousePressEvent(self, *args, **kwargs):
		if not self.clicked_:
			self.setText("Sent")
			self.setStyleSheet("#SendReqButton{background: #ccc; color: #333;}")
			user.server.send_request(self.uid)
			self.clicked_ = False


class Person(QFrame):
	def __init__(self, text, uid, n, box):
		super(Person, self).__init__()
		self.n = n
		self.uid = uid
		self.setObjectName("ContactOff")
		self.layout = QHBoxLayout(self)
		self.avatar = QLabel(text=text[:1].upper())
		self.avatar.setObjectName("Avatar")

		r, g, b = ord(text[0]) % 5 * 60, ord(text[1]) % 5 * 60, ord(text[2]) % 5 * 60
		r2, g2, b2 = 255 - r, 255 - g, 255 -b
		self.setStyleSheet(
			"#Avatar{background:QColor(" + str(r) + "," + str(g) + "," + str(b) + ");\
			color:QColor(" + str(r2) + "," + str(g2) + "," + str(b2) + ");}")
		self.avatar.setFixedSize(32, 32)
		self.layout.addWidget(self.avatar)
		self.layout.addWidget(QLabel(text))
		self.layout.addWidget(SendReqButton(uid, self, box))
		# self.layout.addStretch()
		self.layout.setSpacing(5)

		self._name_text = text

		self.setFixedSize(300, 80)


class PeopleBox(QScrollArea):
	def __init__(self):
		super(PeopleBox, self).__init__()
		self.main_widget = QFrame()
		self.main_widget.setStyleSheet("QFrame{background: #999;}")
		self.main_widget.setFixedWidth(300)
		self.layout = QVBoxLayout(self.main_widget)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.updatePeople([])

		self.setWidget(self.main_widget)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

	def updatePeople(self, people):
		for i in reversed(range(self.layout.count())):
			w = self.layout.takeAt(i)
			self.layout.removeItem(w)
			# w.setParent(None)

		i = 0
		for person in people:
			person_widget = Person(
				text=person[1], uid=person[0], n=i, box=self
			)
			self.layout.addWidget(person_widget)
		self.layout.addStretch()
		self.main_widget.setFixedHeight(len(people) * 80)

	def event(self, event):
		if event.type() == 2222:
			self.updatePeople(event.people)
		else:
			super(PeopleBox, self).event(event)
		return True


class PeopleBlock(QScrollArea):
	def __init__(self):
		super(PeopleBlock, self).__init__()
		widget = QWidget()
		widget.setStyleSheet("QWidget{background: #ccf;}")
		self.people_box = PeopleBox()
		main_layout = QVBoxLayout()
		main_layout.addWidget(self.people_box)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)
		widget.setLayout(main_layout)
		widget.setMinimumWidth(280)
		widget.setFixedHeight(400)
		self.setFixedHeight(400)
		self.setWidget(widget)
