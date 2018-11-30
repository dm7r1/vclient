class UserData:
	def __init__(self):
		# Contact MODEL    UID, Login, (ip, port) last_seen_timestamp, rsa_encrypter
		self.contacts = {
			48951:   (48951,   "Tommy",    ("127.0.0.1", 7777), 459997, "HERE WILL BE RSA ENCRYPTER"),
			456:     (456,     "Vladimir", ("127.0.0.1", 6777), 459997, "HERE WILL BE RSA ENCRYPTER"),
			78979:   (78979,   "Gumball",  ("127.0.0.1", 7737), 459997, "HERE WILL BE RSA ENCRYPTER"),
			2177635: (2177635, "R0B07",    ("127.0.0.1", 7727), 459997, "HERE WILL BE RSA ENCRYPTER"),
			522:     (522,     "N0N4M3",   ("127.0.0.1", 7477), 459997, "HERE WILL BE RSA ENCRYPTER"),
		}
		# Request MODEL    UID, Login
		self.requests = [
		]
