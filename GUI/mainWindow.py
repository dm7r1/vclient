from PySide.QtGui import QMainWindow, QHBoxLayout, QWidget
from .people.left import LeftContainer
from .right import RightContainer
from superdata.us3r import user
from GUI.guiStates import GUIStates


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setWindowTitle("Vector Chat")

		self.setCentralWidget(QWidget())

		main_layout = QHBoxLayout()
		main_layout.setSpacing(0)
		main_layout.setContentsMargins(0, 0, 0, 0)
		self.centralWidget().setLayout(main_layout)

		self.left = LeftContainer()
		main_layout.addWidget(self.left)

		self.right = RightContainer(self)
		main_layout.addWidget(self.right)

		main_layout.addStretch()

		GUIStates.set_widgets(self.right)
		GUIStates.set_user(user)
		self.right.canvas.create_and_star_recv_thread()

		self.setFixedSize(1000, 700)

	def showEvent(self, *args, **kwargs):
		pass

	def call(self):
		self.canvas.setVisible(True)

	def closeEvent(self, *args, **kwargs):
		self.destroy(True, True)
