import sounddevice as sd
from numpy import int16, frombuffer


class AudioInStream:
	def __init__(self, p2p_manager, sock):
		def callback(in_data, frames, time, status):
			if p2p_manager.is_connected:
				for i in range(len(in_data)):
					in_data[i, 0] *= 100               # TODO dynamic K
					in_data[i, 1] *= 100
				sock.sendto(p2p_manager.server_cipher_aes.encrypt(b'\x01' + p2p_manager.connected_uid.to_bytes(4, "big") + p2p_manager.cipher_aes.encrypt(bytearray(in_data))), p2p_manager.server_proxy_addr)
		self.stream = sd.InputStream(samplerate=44100, callback=callback, dtype=int16, channels=2)

	def start(self):
		try:
			self.stream.start()
		except sd.PortAudioError:
			pass

	def stop(self):
		self.stream.stop()


class AudioOutStream:
	def __init__(self, p2p_manager, sock):
		def callback(out_data, frames, time, status):
			if p2p_manager.is_connected:
				data, addr = sock.recvfrom(5000)
				try:
					out_data[:] = frombuffer(p2p_manager.cipher_aes.decrypt(data), dtype=int16).reshape(1136, 2)
				except Exception as e:
					print("sound stream ERR:", str(e))
		self.stream = sd.OutputStream(samplerate=44100, callback=callback, dtype=int16, channels=2)

	def start(self):
		try:
			self.stream.start()
		except sd.PortAudioError:
			pass

	def stop(self):
		self.stream.stop()
