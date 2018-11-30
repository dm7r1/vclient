import threading
from time import sleep


class AbstractNetThread(threading.Thread):
	def __init__(self, net_worker, user, timeout, token):
		super(AbstractNetThread, self).__init__()
		self.net_worker = net_worker
		self.user = user
		self.timeout = timeout
		self.token = token
		self.work = True
		self.daemon = True

	def run(self):
		while self.work:
			self.do()
		sleep(self.timeout)

	def stop(self):
		self.work = False

	def do(self):
		pass
