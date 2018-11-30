from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import pad, unpad
from random import getrandbits


def gen_aes_key_int(size):
	return getrandbits(size * 8)


def gen_aes_key_bytes(size):
	return gen_aes_key_int(size).to_bytes(size, "big")


class CipherAES:
	def __init__(self, key):
		self.encrypter = AES.new(key, AES.MODE_CBC)
		self.decrypter = AES.new(key, AES.MODE_CBC)

	def decrypt(self, encrypted_data):
		return unpad(self.decrypter.decrypt(encrypted_data[8:]), AES.block_size)[AES.block_size:]

	def decrypt_many(self, encrypted_data):
		data = bytearray()
		last_end = 0
		while last_end < len(encrypted_data):
			end = int.from_bytes(encrypted_data[last_end:last_end + 8], "big") + 8 + last_end
			data += self.decrypt(encrypted_data[last_end: end])
			last_end = end
		return data

	def encrypt(self, data):
		enc_data = self.encrypter.encrypt(pad(get_random_bytes(AES.block_size) + data, AES.block_size))
		return len(enc_data).to_bytes(8, "big") + enc_data


class CipherRSA:
	def __init__(self, another_publickey, my_privatekey):
		if another_publickey:
			self.encrypter = PKCS1_OAEP.new(RSA.import_key(another_publickey))
		if my_privatekey:
			self.decrypter = PKCS1_OAEP.new(my_privatekey)

	def encrypt(self, data):
		return self.encrypter.encrypt(data)

	def decrypt(self, data):
		return self.decrypter.decrypt(data)
