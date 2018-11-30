from PySide.QtGui import QLabel
from PySide.QtCore import QEvent
from superdata.us3r import user


class WarningLabel(QLabel):
	def __init__(self):
		super(WarningLabel, self).__init__(
			"I can't see you. "
			"Check the lighting. \n Look into the camera")
		self.setObjectName("WarningLabel")

	def event(self, event):
		if event.type() == 777:
			self.setVisible(True)
			return True
		elif event.type() == 778:
			self.setVisible(False)
			return True
		else:
			return super(WarningLabel, self).event(event)

	def showIt(self):
		user.qtapp.postEvent(self, QEvent(QEvent.Type(777)))

	def hideIt(self):
		user.qtapp.postEvent(self, QEvent(QEvent.Type(778)))
