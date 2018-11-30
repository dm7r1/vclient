from PySide.QtGui import QFrame, QLabel
from PySide.QtCore import Qt, QEvent
from .warningLabel import WarningLabel
from .canvasGL import CanvasGL
from superdata.us3r import user
from GUI.guiStates import GUIStates
from .buttons import TextButton
from .buttonsImpl import RemoveButton, StopButton, CallButton, SettingsButton


class RightContainer(QFrame):
	def __init__(self, main_window):
		super(RightContainer, self).__init__()

		self.setFixedWidth(780)
		self.setObjectName("Right")

		vertical_line = QFrame()
		vertical_line.setParent(self)
		vertical_line.setObjectName("BigVerticalLine")
		vertical_line.setFixedSize(2, 645)
		vertical_line.move(0, 30)

		b_contacts = TextButton(main_window.left.show_contacts, "contacts")
		b_reqs = TextButton(main_window.left.show_requests, "requests")
		b_search = TextButton(main_window.left.show_people, "people")

		self.settings_button = SettingsButton()
		self.remove_button = RemoveButton()
		self.remove_button.setVisible(False)

		pos_y = 10
		for button in b_contacts, b_reqs, b_search, self.settings_button, self.remove_button:
			button.setParent(self)
			button.move(610, pos_y)
			button.setFixedSize(120, 50)
			button.setAlignment(Qt.AlignRight)
			pos_y += 50

		self.remove_button.move(610, 650)

		self.canvas = CanvasGL()
		self.canvas.setParent(self)
		self.canvas.move(60, 40)
		self.canvas.setFixedSize(500, 550)
		self.canvas.setVisible(True)

		self.call_button = CallButton()
		self.call_button.setVisible(False)
		self.stop_button = StopButton()

		for button in self.call_button, self.stop_button:
			button.setParent(self)
			button.move(284, 620)

		self.stop_button.setVisible(False)
		self.login_label = QLabel()
		self.login_label.setObjectName("LoginLabel")
		self.login_label.setParent(self)
		self.login_label.move(250, 10)
		self.login_label.setFixedSize(120, 20)
		self.login_label.setAlignment(Qt.AlignCenter)
		self.login_label.setVisible(False)

		self.warning_label = WarningLabel()
		self.warning_label.setParent(self)
		self.warning_label.move(80, 70)
		self.warning_label.setVisible(False)

	def event(self, event):
		if event.type() == 666:
			self.call_button.setVisible(True)
			self.stop_button.setVisible(False)
			self.remove_button.setVisible(True)
			self.login_label.setVisible(True)
			self.login_label.setText(user.get_contact(GUIStates.get_contact_id())[1])
			return True
		elif event.type() == 777:
			self.call_button.setVisible(False)
			self.stop_button.setVisible(False)
			self.remove_button.setVisible(False)
			self.login_label.setVisible(False)
			return True
		elif event.type() == 888:
			self.canvas.showIt()
			self.login_label.setVisible(True)
			self.login_label.setText(user.get_contact(event.uid)[1])
			return True
		else:
			return super(RightContainer, self).event(event)

	def post_set_contact(self):
		if GUIStates.get_contact_id() == GUIStates.NO_CONTACT:
			user.qtapp.postEvent(self, QEvent(QEvent.Type(777)))
		else:
			user.qtapp.postEvent(self, QEvent(QEvent.Type(666)))

	def post_set_call(self, uid):
		qevent = QEvent(QEvent.Type(888))
		qevent.uid = uid
		user.qtapp.postEvent(self, qevent)
