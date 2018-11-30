from .netWorker import NetWorker
from .async_net.getThread import GetThread
from socket import error as sock_error
import settings
import client.codes as codes
from encryption import gen_aes_key_int, CipherRSA
from Cryptodome.PublicKey import RSA


class MainClient:
	KEY_SIZE = 16

	def __init__(self, user, in_port):
		self.net_worker = object()  # NetWorker(address=settings.address, port=settings.mainPort, key=object())
		self.user = user
		self.token = ""

		self.in_port = in_port

	def send2server(self, operation, data):
		data["operation"] = operation
		data["token"] = self.token
		data["id"] = self.user.id
		self.net_worker.send(data)

	def remove_friend(self, uid):
		self.send2server("remove_friend", {"uid": uid})

	def send_request(self, uid):
		self.send2server("send_request", {"uid": uid})

	def add_to_contacts(self, uid):
		self.send2server("add_to_contacts", {"uid": uid})

	def search_people(self, q):
		self.send2server("search_people", {"q": q})

	def get_requests(self):
		self.send2server("get_requests", {})

	def log_in(self, login, password):
		try:
			session_key = gen_aes_key_int(MainClient.KEY_SIZE)
			self.net_worker = NetWorker(address=settings.address, port=settings.mainPort, key=session_key.to_bytes(MainClient.KEY_SIZE, "big"))
			self.net_worker.connect()
			self.net_worker.send({"operation": "get_pubkey"}, encrypt=False)
			res = self.net_worker.receive(1024, decrypt=False)
			encrypter_rsa = CipherRSA(res["key"].encode(), None)
			user_rsa_key = RSA.generate(2048)
			self.user.pconn_manager.set_rsa_decrypter(CipherRSA(None, user_rsa_key))

			self.net_worker.send({"operation": "log_in", "data": {
																"login": login,
																"password": password,
																"port": self.in_port,
																"session_key": session_key
									}
								}, special_cipher=encrypter_rsa)
			res = self.net_worker.receive(8196)
			if res["result"] == "pubkey_left":
				self.user.id = res["id"]
				self.token = res["token"]
				self.send2server("set_user_pubkey", {
													"user_pubkey": user_rsa_key.publickey().export_key().decode()
				})
				self.user.set_contacts_from_list([])

				thread = GetThread(self.net_worker, self.user, self.token)
				self.thread = thread

				return codes.LOGGED_IN
			else:
				self.net_worker.close()

			if res["result"] == "invalid":
				return codes.WRONG_DATA

			if res["result"] == "busy":
				return codes.BUSY_USER
		except sock_error as err:
			if err.errno == 10061:
				return codes.NO_SERVER_CONNECTION

		return codes.UNEXPECTED_PROBLEM

	def start(self):
		self.thread.start()

	def stop_close(self):
		self.thread.stop()
		self.net_worker.close()

