import sounddevice as sd
from numpy import int16, frombuffer
import socket
from tkinter import *
import numpy as np
import time
import scipy.fftpack
import matplotlib.pyplot as plt

root = Tk()


m = 10
def that_func(y):
	yf = scipy.fftpack.fft(y)
	xf = np.arange(len(y))

	fig, ax = plt.subplots()
	ax.plot(xf, np.abs(yf.real), 'r')
	ax.plot(xf, -np.abs(yf.imag), 'b')

	plt.show()

	time.sleep(1000)


	if 1:
		for i in range(m, len(yf) // 2):
			yf[i - m] = yf[i]
			yf[i] = 0

		for i in reversed(range(len(yf) // 2, len(yf) - m)):
			yf[i + m] = yf[i]
			yf[i] = 0

	yy = scipy.fftpack.ifft(yf)
	return yy




canvas_width = 800
canvas_height = 400
w = Canvas(root, width=canvas_width,	height=canvas_height)
w.pack()

dttd = bytes()


def loop2():
	w.delete("all")
	for x in range(len(dttd)):
		for c in range(1):
			w.create_rectangle(x, dttd[x][c].real * 3000 + 200, x, dttd[x][c].real * 3000 + 200, outline=("red", "green")[c])
	root.after(400, loop2)


audio_data = []

interp_k = 8


def change(data):
	global dttd
	data2 = data
	print(data)
	print("XX", that_func(data))
	data2 = that_func(data, )
	dttd = data2
	return data2


class AudioInStream:
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		def callback(in_data, frames, time, status):
			in_data = change(in_data)
			audio_data.append(in_data)
		self.stream = sd.InputStream(samplerate=44100, callback=callback, dtype=int16, channels=1)
		self.stream.start()


class AudioOutStream:
	def __init__(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(("127.0.0.1", 90))

		def callback(out_data, frames, time, status):
			global run
			if len(audio_data) == 0:
				self.stream.stop()
				run = False
				return
			data = audio_data.pop(0)
			print(data)
			# out_data[:] = frombuffer(data, dtype=int16).reshape(1136, 1)
			np.asarray((data.reshape(1136, 1) + 1) * 1000, dtype=int16)
		self.stream = sd.OutputStream(samplerate=44100, callback=callback, dtype=int16, channels=1)
		self.stream.start()


ais = AudioInStream()


# melody = str(input())
#loop2()
#mainloop()
ais.stream.stop()

aos = AudioOutStream()


run = True
while run:
	pass
