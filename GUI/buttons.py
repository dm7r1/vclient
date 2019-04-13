from PySide.QtGui import QLabel, QFrame, QSizePolicy
from PySide.QtCore import Qt


class TextButton(QFrame):
	def __init__(self, click_func, text):
		super(TextButton, self).__init__()
		self.onClick = click_func
		self.label = QLabel(text)
		self.label.setParent(self)
		self.label.setObjectName("TextButton")
		self.setFixedSize(120, 36)

	def setAlignment(self, alignment):
		self.label.setAlignment(alignment)

	def setFixedSize(self, w, h):
		super(TextButton, self).setFixedSize(w, h)
		self.label.setFixedSize(w, h)

	def onClick(self):
		pass

	def mousePressEvent(self, *args, **kwargs):
		self.onClick()


class CircleButton(QFrame):
	def __init__(self, click_func, text=None, css_label_name=None, css_circle_name=None):
		super(CircleButton, self).__init__()
		self.onClick = click_func
		self.setFixedSize(64, 64)
		self.label = QLabel()
		self.label.setParent(self)
		self.label.setFixedSize(64, 58)
		self.label.setAlignment(Qt.AlignCenter)

		if css_label_name:
			self.label.setObjectName(css_label_name)
		if css_circle_name:
			self.setObjectName(css_circle_name)
		if text:
			self.label.setText(text)

	def onClick(self):
		pass

	def mousePressEvent(self, *args, **kwargs):
		self.onClick()


class AddButton(CircleButton):
	def __init__(self, click_func):
		def click_func_custom():
			click_func()
			self.setVisible(False)
		super(AddButton, self).__init__(
			click_func_custom, text="add",
			css_label_name="GreenTextButtonSmall")
		self.setFixedSize(48, 48)
		self.label.setFixedSize(48, 48)