from socket import socket, AF_INET, SOCK_DGRAM
from threads.points_threads import PointsSendThread, PointsReceiveThread
from threads.audio_streams import AudioInStream, AudioOutStream
from threads.threads_storage import Threads
import avatar_settings
import threading
from encryption import gen_aes_key_bytes, CipherAES
import settings
import pickle

#   P2P DATA MODEL
#   18 + KEY_SIZE * 2  bytes
#   ( @ #### PP VV KKKKK... )x2
#   where @ - command, #### - user id, PP - pts socket port, VV - voice socket port, KKKKK... - key

KEY_SIZE = 16
PACKET_SIZE = 18 + KEY_SIZE * 2
ENCRYPTED_PACKET_SIZE = 500


class Commands:
	CALL = 0
	STOP_REQ = 1
	ACCEPT = 2
	STOP = 3


class P2PManager:

	def __init__(self, user):
		self.user = user

		self.server_proxy_addr = settings.server_address, settings.proxy_server_port

		self.manager_socket = socket(AF_INET, SOCK_DGRAM)
		self.manager_socket.bind(("", 0))
		self.pts_socket = socket(AF_INET, SOCK_DGRAM)
		self.pts_socket.bind(("", 0))
		self.voice_socket = socket(AF_INET, SOCK_DGRAM)
		self.voice_socket.bind(("", 0))

		self.in_calls = {}

		self.is_connected = False  # calling or connected
		self.is_calling = False    # calling

		self.connected_uid = -1
		self.connected_pts_addr = ()
		self.connected_voice_addr = ()
		self.connected_addr = ()

		self.key = bytes()
		self.cipher_aes = object()
		self.decrypter_rsa = object()
		self.server_cipher_aes = object()

		self.in_handler = InHandler(self.manager_socket, self, self.user)
		self.in_handler.start()

		Threads.set_send_pts_thread(PointsSendThread(self.pts_socket, self.user))
		Threads.set_audio_streams(AudioInStream(self, self.voice_socket), AudioOutStream(self, self.voice_socket))

	def send_ports(self):
		self.manager_socket.sendto(self.server_cipher_aes.encrypt(b'\x03'), self.server_proxy_addr)
		self.voice_socket.sendto(self.server_cipher_aes.encrypt(b'\x04'), self.server_proxy_addr)
		self.pts_socket.sendto(self.server_cipher_aes.encrypt(b'\x05'), self.server_proxy_addr)

	def set_server_cipher_aes(self, cipher_aes):
		self.server_cipher_aes = cipher_aes

	def set_rsa_decrypter(self, decrypter):
		self.decrypter_rsa = decrypter

	def get_in_port(self):
		print(self.manager_socket.getsockname())
		return self.manager_socket.getsockname()[1]

	def get_in_pts_port(self):
		return self.pts_socket.getsockname()[1]

	def get_in_voice_port(self):
		return self.voice_socket.getsockname()[1]

	def make_pts_receive_thread(self, widget):
		return PointsReceiveThread(socket=self.pts_socket, widget=widget, user=self.user)

	def call(self, uid):
		if not self.is_connected:
			another_user = self.user.get_contact(uid)
			addr = another_user[2]
			self.send(Commands.CALL, uid, self.get_in_pts_port(), self.get_in_voice_port())
			self.set_calling(uid, addr)
			print("CALLING", addr)

	def accept(self, uid):
		if (not self.is_connected or self.connected_uid == self.user.id) and uid in self.in_calls:
			another_user = self.user.get_contact(uid)
			addr = another_user[2]
			key = gen_aes_key_bytes(KEY_SIZE)
			self.send(Commands.ACCEPT, uid, self.get_in_pts_port(), self.get_in_voice_port(), key)
			in_call = self.in_calls[uid]
			self.set_connected(uid, addr, in_call[0], in_call[1], key)
			del self.in_calls[uid]

	def refuse(self, uid):
		self.send(Commands.STOP, self.connected_uid)

	def stop_req(self):
		self.send(Commands.STOP_REQ, self.connected_uid)
		self.disconnect()

	def stop(self):
		self.send(Commands.STOP, self.connected_uid)
		self.disconnect()

	def send(self, command, uid, pts_port=0, voice_port=0, key=bytes(KEY_SIZE)):
		print(self.manager_socket.getsockname(),":::")
		self.manager_socket.sendto(
			self.server_cipher_aes.encrypt(b'\x00' + uid.to_bytes(4, 'big') +
			self.user.get_contact(uid)[4].encrypt(self.pack(command, self.user.id, pts_port, voice_port, key) * 2)), self.server_proxy_addr
		)

	def set_connected(self, uid, addr, pport, vport, key):
		self.is_connected = True
		self.connected_uid = uid
		self.connected_addr = addr
		self.connected_pts_addr = addr[0], pport
		self.connected_voice_addr = addr[0], vport
		avatar_settings.another_avatar_ss = avatar_settings.SharedSettings.from_string(self.user.get_contact(uid)[5])

		self.cipher_aes = CipherAES(key)

		self.is_calling = False

		self.user.call_gui(uid)
		Threads.start_audio_streams()
		if avatar_settings.avatar_settings.show_avatar:
			Threads.send_pts_thread.start()

	def set_calling(self, uid, addr):
		self.is_calling = True
		self.is_connected = True
		self.connected_uid = uid
		self.connected_addr = addr

	def disconnect(self):
		self.is_connected = False
		self.is_calling = False
		Threads.send_pts_thread.close()
		Threads.send_pts_thread.terminate()
		Threads.stop_audio_streams()

	@staticmethod
	def pack(command, uid, pts_port, voice_port, key):
		return bytearray([command]) + uid.to_bytes(4, "big") + pts_port.to_bytes(2, "big") + voice_port.to_bytes(2, "big") + key

	@staticmethod
	def unpack(data):
		command = data[0]
		uid = int.from_bytes(data[1:5], "big")
		pts_port = int.from_bytes(data[5:7], "big")
		voice_port = int.from_bytes(data[7:9], "big")
		key = data[9:9 + KEY_SIZE]
		return command, uid, pts_port, voice_port, key


class InHandler(threading.Thread):
	def __init__(self, sock: socket, owner: P2PManager, user):
		super(InHandler, self).__init__()
		self.user = user
		self._sock = sock
		self._p2p_manager = owner
		self._in_calls = []

	def run(self):
		while True:
			try:
				data, addr = self._sock.recvfrom(ENCRYPTED_PACKET_SIZE)
				data = self._p2p_manager.decrypter_rsa.decrypt(data)
			except Exception:
				return

			if data[len(data) // 2:] != data[:len(data) // 2]:   # check packet is not broken
				print("broken packet")
				return

			data = data[:len(data) // 2]
			command, uid, pts_port, voice_port, key = self._p2p_manager.unpack(data)

			if not self.valid_friend(uid):
				return

			if command == Commands.CALL:
				self._p2p_manager.in_calls[uid] = (pts_port, voice_port)
				self.user.main_window.left.in_calls_layout.post_new_call(uid)
			elif command == Commands.STOP_REQ:
				if uid in self._p2p_manager.in_calls:
					del self._p2p_manager.in_calls[uid]
					self.user.main_window.left.in_calls_layout.post_remove_call(uid)
			elif command == Commands.ACCEPT:
				if self._p2p_manager.connected_uid == uid:
					self._p2p_manager.set_connected(uid, addr, pts_port, voice_port, key)
			elif command == Commands.STOP:
				self.user.stop_call_gui()
				self._p2p_manager.disconnect()

	def valid_friend(self, uid):
		curr_user = self.user.get_contact(uid)
		return curr_user

	def valid_accept(self, uid, addr):
		return uid == self._p2p_manager.connected_uid == uid