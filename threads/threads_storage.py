class Threads:
	recv_pts_thread = object()
	send_pts_thread = object()
	audio_in_stream = object()
	audio_out_stream = object()

	@staticmethod
	def set_audio_streams(audio_in_stream, audio_out_stream):
		Threads.audio_in_stream = audio_in_stream
		Threads.audio_out_stream = audio_out_stream

	@staticmethod
	def start_audio_streams():
		Threads.audio_in_stream.start()
		Threads.audio_out_stream.start()

	@staticmethod
	def stop_audio_streams():
		Threads.audio_in_stream.stop()
		Threads.audio_out_stream.stop()

	@staticmethod
	def set_recv_pts_thread(thread):
		Threads.recv_pts_thread = thread

	@staticmethod
	def set_send_pts_thread(thread):
		Threads.send_pts_thread = thread

	@staticmethod
	def stop_threads():
		Threads.recv_pts_thread.off()
		Threads.send_pts_thread.off()


