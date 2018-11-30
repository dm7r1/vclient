from PySide.QtGui import QFrame, QPainter, QBrush, QPen, QColor
from math import pi


class Avatar(QFrame):
	def __init__(self):
		super(Avatar, self).__init__()
		self.setObjectName("Avatar")
		self.setFixedSize(32, 32)
