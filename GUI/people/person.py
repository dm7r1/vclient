from PySide.QtGui import QFrame, QHBoxLayout, QVBoxLayout, QLabel


class Person(QFrame):
	def __init__(self, name):
		super(Person, self).__init__()
		self.setObjectName("PersonBox")
		self.main = QHBoxLayout()
		self.main.setContentsMargins(4, 0, 0, 0)
		self.setLayout(self.main)
		self.left = QVBoxLayout()
		self.left.setSpacing(0)
		self.left.setContentsMargins(0, 0, 0, 0)
		self.name = QLabel(name)
		self.name.setFixedHeight(36)
		self.name.setObjectName("PersonName")
		self.left.addWidget(self.name)
		self.main.addLayout(self.left)
		self.setFixedSize(250, 54)

