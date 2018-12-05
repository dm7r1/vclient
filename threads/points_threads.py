from PySide.QtCore import QThread, QEvent
from DModule.drawingModel import DrawingModel
from time import sleep, time
from numpy import ndarray
from .pfinder_instance import pf


class CustomThread(QThread):
	_work = 0

	def start(self):
		self._work = 1
		super(CustomThread, self).start()

	def off(self, forced=False):
		self._work = 0
		if not forced:
			self.wait()

	def switch(self):
		if self._work:
			self.off()
		else:
			self.on()

	def _loop(self):
		pass

	def _end(self):
		pass

	def _start(self):
		pass

	def run(self, *args, **kwargs):
		self._start()
		while self._work:
			sleep(0.01)
			self._loop()
		self._end()


DATA_SIZE = 168  # size of encrypted array of points
PTS = 70


class PointsReceiveThread(CustomThread):
	def __init__(self, widget, socket, user):
		super(PointsReceiveThread, self).__init__()
		self._socket = socket
		self._widget = widget

		self.user = user

		self.dmodel = DrawingModel(1, 1)

	def _loop(self):
		data, addr = self._socket.recvfrom(DATA_SIZE)
		if not self.user.pconn_manager.is_connected:
			return

		polygons = self.handle_data(self.user.pconn_manager.cipher_aes.decrypt(data))
		if polygons:
			self._widget._polygons = polygons
			self._widget.update()

	def handle_data(self, data):
		pts = ndarray(shape=(300, 2))
		i = 0
		while i < PTS:
			pts[i, 0] = data[i * 2]
			pts[i, 1] = data[i * 2 + 1]
			i += 1
		return self.dmodel.process(pts)

	def stop_call(self):
		self.addresses.remove(self.user.pconn_manager.from_addr)
		self.user.qtapp.postEvent(self._widget, QEvent(QEvent.Type(999)))


class PointsSendThread(CustomThread):
	def __init__(self, socket, user):
		super(PointsSendThread, self).__init__()
		self.user = user
		self._socket = socket

		self.points_finder = pf

		self.t = 0
		self.first = True
		self.showed = False

	@staticmethod
	def to255(a):
		return 255 if a > 255 else a

	def _loop(self):
		pts = self.points_finder.get_points()
		if len(pts) == 0:
			if not self.first:
				if not self.showed and time() - self.t > 0.5:
					self.user.main_window.right.warning_label.showIt()
					self.showed = True
			else:
				self.first = False
				self.t = time()
		else:
			self.user.main_window.right.warning_label.hideIt()
			if not self.first:
				self.first = True
				self.showed = False

			data = bytearray(PTS * 2)
			for i in range(PTS):
				data[i * 2] = self.to255(pts[i][0])
				data[i * 2 + 1] = self.to255(pts[i][1])
			self._socket.sendto(self.user.pconn_manager.server_cipher_aes.encrypt(b'\x02' + self.user.pconn_manager.connected_uid.to_bytes(4, "big") + self.user.pconn_manager.cipher_aes.encrypt(data)), self.user.pconn_manager.server_proxy_addr)

	def close(self):
		self.points_finder.release_cam()

	def _end(self):
		self.close()

	def _start(self):
		self.first = True
		self.showed = False
		self.t = 0
		self.points_finder.open_cam()

