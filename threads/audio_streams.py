import sounddevice as sd
from numpy import int16, frombuffer


class AudioInStream:
	def __init__(self, p2p_manager, sock):
		def callback(in_data, frames, time, status):
			if p2p_manager.is_connected:
				sock.sendto(p2p_manager.cipher_aes.encrypt(bytearray(in_data)), p2p_manager.connected_voice_addr)
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
				data, addr = sock.recvfrom(50000)
				if addr == p2p_manager.connected_voice_addr:
					out_data[:] = frombuffer(p2p_manager.cipher_aes.decrypt(data), dtype=int16).reshape(1136, 2)
		self.stream = sd.OutputStream(samplerate=44100, callback=callback, dtype=int16, channels=2)

	def start(self):
		try:
			self.stream.start()
		except sd.PortAudioError:
			pass

	def stop(self):
		self.stream.stop()
