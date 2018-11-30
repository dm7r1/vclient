from PySide.QtGui import QMainWindow, QVBoxLayout, QLineEdit, QWidget, QCheckBox, QPushButton
from PySide.QtCore import Qt
import client.codes as codes


class AuthorizationWindow(QMainWindow):
	def __init__(self, usr):
		super(AuthorizationWindow, self).__init__()
		self.setWindowTitle("Vector Chat")

		self.setMinimumWidth(300)
		self.code = codes.NO_DATA
		self.usr = usr

		main_layout = QVBoxLayout()

		self.login_field = QLineEdit()
		self.login_field.setPlaceholderText("login")
		main_layout.addWidget(self.login_field)

		self.pass_field = QLineEdit()
		self.pass_field.setEchoMode(QLineEdit.Password)
		self.pass_field.setPlaceholderText("password")
		main_layout.addWidget(self.pass_field)

		self.remember = QCheckBox()
		self.remember.setText("remember me")
		main_layout.addWidget(self.remember)

		self.send_btn = QPushButton()
		self.send_btn.setText("Sign in")
		self.send_btn.clicked.connect(self.send_clicked)
		main_layout.addWidget(self.send_btn)

		self.setCentralWidget(QWidget())
		self.centralWidget().setLayout(main_layout)

	def send_clicked(self):
		print("send")
		login, password = self.login_field.text(), self.pass_field.text()
		if login == "" or password == "":
			return
		self.usr.set_user_data(login, password)
		self.code = self.usr.log_in_(self.remember.checkState() == Qt.Checked)
		if self.code == codes.LOGGED_IN:
			self.close()

	def get_code(self):
		return self.code