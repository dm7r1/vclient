from PySide.QtGui import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QFrame
from PySide.QtCore import QEvent, Qt
from .buttonsImpl import RefuseButton, AcceptButton, TextButton
from superdata.us3r import user
from utils.utils import remove_layout


class InCall(QVBoxLayout):
	def __init__(self, uid):
		super(InCall, self).__init__()
		self.setSpacing(0)
		person = user.get_contact(uid)
		self.uid = uid
		self.label_incoming_call_text = QLabel("incoming call from")
		self.label_incoming_call_text.setObjectName("IncomingCallText")
		self.addWidget(self.label_incoming_call_text)
		self.label_name = QLabel(person[1])
		self.label_name.setObjectName("IncomingCallUsername")
		self.addWidget(self.label_name)

		self.buttons_layout = QHBoxLayout()
		self.buttons_layout.setSpacing(16)
		self.buttons_layout.setContentsMargins(0, 0, 0, 0)
		self.accept_button = AcceptButton(uid, self)
		self.accept_button.setAlignment(Qt.AlignLeft)
		# separator_line = QFrame()
		# separator_line.setObjectName("LittleVerticalLine")
		# separator_line.setFixedSize(2, 28)
		self.refuse_button = RefuseButton(uid, self)
		self.refuse_button.setAlignment(Qt.AlignRight)
		self.buttons_layout.addWidget(self.refuse_button)
		# self.buttons_layout.addWidget(separator_line)
		self.buttons_layout.addWidget(self.accept_button)
		self.addLayout(self.buttons_layout)

	def remove_me(self):
		qevent = QEvent(QEvent.Type(666))
		qevent.uid = self.uid
		user.qtapp.postEvent(user.main_window.left.in_calls_layout, qevent)


class InCallsLayout(QWidget):
	def __init__(self):
		super(InCallsLayout, self).__init__()
		self.main = QVBoxLayout()
		self.setLayout(self.main)
		self.main.setAlignment(Qt.AlignTop)

	def event(self, event):
		if event.type() == 555:
			self.main.addLayout(InCall(event.uid))
			self.setFixedHeight(self.height() + 120)
			return True
		elif event.type() == 666:
			self.setFixedHeight(self.height() - 120)
			for i in range(self.main.count()):
				in_call = self.main.takeAt(i)
				if in_call.uid == event.uid:
					remove_layout(in_call)
			return True
		else:
			return super(InCallsLayout, self).event(event)

	def post_new_call(self, uid):
		qevent = QEvent(QEvent.Type(555))
		qevent.uid = uid
		user.qtapp.postEvent(self, qevent)

	def post_remove_call(self, uid):
		qevent = QEvent(QEvent.Type(666))
		qevent.uid = uid
		user.qtapp.postEvent(self, qevent)
