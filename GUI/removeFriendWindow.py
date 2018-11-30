from PySide.QtGui import QMainWindow, QPushButton, QFrame, QGridLayout, QLabel
from PySide.QtCore import Qt
from .buttonsImpl import TextButton
from superdata.us3r import user


class RemoveButton(TextButton):
	def __init__(self, uid, window):
		def del_func():
			user.server.remove_friend(uid)
			window.close()

		super(RemoveButton, self).__init__(del_func, "Yes")
		self.setAlignment(Qt.AlignCenter)


class CancelButton(TextButton):
	def __init__(self, window):
		def cancel_func():
			window.close()

		super(CancelButton, self).__init__(cancel_func, "No")
		self.setAlignment(Qt.AlignCenter)


class RemoveFriendWindow(QMainWindow):
	def __init__(self, uid):
		super(RemoveFriendWindow, self).__init__()
		self.setWindowTitle("Are you sure?")
		self.uid = uid
		widget = QFrame()
		layout = QGridLayout()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		layout.addWidget(QLabel("Are you sure you want to delete " + user.get_contact(uid)[1] + " from your contacts"), 0, 0, 1, 2)
		layout.addWidget(RemoveButton(uid, self), 1, 0, 1, 1)
		layout.addWidget(CancelButton(self), 1, 1, 1, 1)
