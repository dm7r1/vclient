import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from time import time as tt
import sounddevice as sd
from numpy import int16, frombuffer
from scipy.io import wavfile

m = 20
def that_func(y, n, t):
	yf = scipy.fftpack.fft(y)
	print(yf.shape)
	xf = np.arange(n)
	print(xf.shape)

	fig, ax = plt.subplots()
	ax.plot(xf, yf.real, 'r')
	ax.plot(xf, yf.imag, 'b')

	if 1:
		if 0:
			for i in reversed(range(len(yf) // 2 - m)):
				yf[i + m] = yf[i]
				yf[i] = 0

			for i in range(len(yf) // 2 + m, len(yf)):
				yf[i - m] = yf[i]
				yf[i] = 0
		else:
			for i in range(m, len(yf) // 2):
				yf[i - m] = yf[i]
				if yf[i] > 100 * 1000 * 1000:
					print(i, ">>", i - m)
				yf[i] = 0

			for i in reversed(range(len(yf) // 2, len(yf) - m)):
				yf[i + m] = yf[i]
				if yf[i] > 10 * 1000 * 1000:
					print(i, ">>", i + m)
				yf[i] = 0

	# yf[13000] = complex(15000, 0)
	# yf[60000] = complex(0, 15000)


	yy = scipy.fftpack.ifft(yf)
	fig, ax = plt.subplots()
	ax.plot(xf, yy, 'g')

	return yy


N = 151263
N = 1136*10
N = 8196 * 8
T = 1.0
x = np.linspace(0.0, N*T, N)
fs = 44100
y = np.cos(x / fs * (2.0 * np.pi) * 100)*10000

fs, data = wavfile.read("test2.wav")
# y = data
fig, ax = plt.subplots()
ax.plot(x, y)
yy = that_func(y, N, T)

it = 0

def callback(out_data, frames, time, status):
	global it
	if it + 1136 > len(yy):
		it = 0
	yyy = y[it:it+1136]
	it += 1136
	out_data[:] = np.asarray(yyy.reshape(1136, 1), dtype=int16)


stream = sd.OutputStream(samplerate=44100, callback=callback, dtype=int16, channels=1)
stream.start()

plt.show()
input()