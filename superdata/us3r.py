from client.mainclient import MainClient
from superdata.us3rData import UserData
from client.p2p_manager import P2PManager
from GUI.authorizationWindow import AuthorizationWindow
from GUI.guiStates import GUIStates
import sys
from utils.utils import read_all
from PySide.QtGui import QApplication, QIcon
from hashlib import sha256
from os.path import isfile
import client.codes as codes
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


class User:
	def __init__(self):
		self.user_data = UserData()

		self.password = ""
		self.login = ""
		self.load_udata()

		self.id = -1

		self.pconn_manager = P2PManager(self)
		self.server = MainClient(self, in_port=self.pconn_manager.get_in_port())
		self.qtapp = object()
		self.main_window = object()

	def set_main_window(self, main_window):
		self.main_window = main_window

	def get_contacts(self):
		return self.user_data.contacts.values()

	def get_contact(self, uid):
		if self.contact_exists(uid):
			return self.user_data.contacts[uid]
		return False

	def contact_exists(self, uid):
		return uid in self.user_data.contacts

	def get_contact_by_addr(self, addr):
		for contact in self.user_data.contacts.values():
			if contact[2] == addr:
				return contact
		return False

	def set_contacts_from_list(self, contacts):
		self.user_data.contacts = {}
		for contact in contacts:
			self.user_data.contacts[contact[0]] = contact[0], contact[1], (contact[3], contact[4]), contact[2], None if len(contact[5]) == 0 else PKCS1_OAEP.new(RSA.import_key(contact[5].encode()))

	def set_requests(self, requests):
		self.user_data.requests = requests

	def get_requests(self):
		return self.user_data.requests

	def set_user_data(self, login, password):
		self.login = login
		self.password = sha256(password.encode()).hexdigest()

	@staticmethod
	def _is_valid(login, password = ""):
		return True

	def log_in(self):
		app = QApplication(sys.argv)
		app.setStyleSheet(
			read_all("resources/css/style.css") +
			read_all("resources/css/style_contacts.css") +
			read_all("resources/css/style_buttons.css") +
			read_all("resources/css/style_calls.css")
		)
		app.setWindowIcon(QIcon("resources/icons/V.png"))
		self.qtapp = app
		if self.log_in_() == codes.LOGGED_IN:
			return codes.LOGGED_IN, app
		authorizationWindow = AuthorizationWindow(self)
		authorizationWindow.move(500, 500)
		authorizationWindow.show()
		app.exec_()
		return authorizationWindow.get_code(), app

	def log_in_(self, save=False):
		if self.login == "" or self.password == "":
			return codes.NO_DATA
		result = self.server.log_in(self.login, self.password)
		if result == codes.LOGGED_IN and save:
			self.save_udata()
		return result

	def call(self, uid):
		self.pconn_manager.call(uid)
		self.call_gui(uid)

	def call_gui(self, uid):
		self.main_window.right.post_set_call(uid)

	def stop_req(self):
		self.pconn_manager.stop_req()

	def stop_call(self):
		self.stop_call_gui()
		self.pconn_manager.stop()

	def stop_call_gui(self):
		self.main_window.right.canvas.hideIt()
		self.main_window.right.warning_label.hideIt()
		GUIStates.set_contact_id(GUIStates.get_contact_id())

	def accept(self, uid):
		self.pconn_manager.accept(uid)

	def refuse(self, uid):
		self.pconn_manager.refuse(uid)

	def load_udata(self):
		if isfile("udata"):
			try:
				with open("udata", "r") as f:
					self.login = f.readline().strip()
					self.password = f.readline().strip()
					return
			except IOError:
				pass
		self.login = ""
		self.password = ""

	def save_udata(self):
		try:
			with open("udata", "w") as f:
				f.writelines([self.login, "\n", self.password])
		except IOError:
			pass


user = User()
