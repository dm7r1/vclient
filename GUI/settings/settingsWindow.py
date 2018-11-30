from PySide.QtGui import QMainWindow, QLabel, QWidget

import sounddevice as sd


class SettingsWindow(QMainWindow):
	def __init__(self):
		super(SettingsWindow, self).__init__()
		self.setWindowTitle("Settings")
		self.setFixedSize(400, 400)

	def showEvent(self, *args, **kwargs):
		pass

