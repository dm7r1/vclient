import socket
from encryption import CipherAES
from utils.parsejson import object2bjson, bjson2object, bjson2objects


class NetWorker:
	def __init__(self, address, port, key):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(True)
		self.port = port
		self.address = address

		self.cipher_aes = CipherAES(key)

	def connect(self):
		self.sock.connect((self.address, self.port))
		print(self.sock.getsockname())

	def send(self, data, special_cipher=None, encrypt=True):
		req = object2bjson(data)
		if encrypt:
			if special_cipher:
				req = special_cipher.encrypt(req)
			else:
				req = self.cipher_aes.encrypt(req)
		self.sock.send(req)

	def receive(self, size=128, decrypt=True):
		data = self.sock.recv(size)
		if decrypt:
			data = self.cipher_aes.decrypt(data)
		return bjson2object(data)

	def receive_many(self, size=128):
		return bjson2objects(self.cipher_aes.decrypt_many(self.sock.recv(size)))

	def close(self):
		self.sock.close()

	def detach(self):
		self.sock.detach()

