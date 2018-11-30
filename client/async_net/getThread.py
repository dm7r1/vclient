from client.async_net.abstractNetThread import AbstractNetThread
from PySide.QtCore import QEvent


class GetThread(AbstractNetThread):
	def __init__(self, net_worker, user, token):
		super(GetThread, self).__init__(net_worker, user, 0.5, token)
		self.data = {}

	def do(self):
		data = self.net_worker.receive_many(8192)
		for self.data in data:
			operation = self.data["operation"]
			if operation == "get_msg":
				self.handle_msgs()
			elif operation == "get_contacts":
				self.handle_contacts()
			elif operation == "get_requests":
				self.handle_requests()
			elif operation == "search_people":
				self.handle_searched_people()

	def handle_msgs(self):
		pass

	def handle_searched_people(self):
		qevent = QEvent(QEvent.Type(2222))

		self.user.main_window.left.people.set_people(self.data["people"])
		self.user.main_window.left.people.post_event_update()

	def handle_contacts(self):
		self.user.set_contacts_from_list(self.data["contacts"])
		self.user.main_window.left.contacts.set_people(self.user.get_contacts())
		self.user.main_window.left.contacts.post_event_update()

	def handle_requests(self):
		self.user.set_requests(self.data["requests"])
		self.user.main_window.left.requests.set_people(self.user.get_requests())
		self.user.main_window.left.requests.post_event_update()
