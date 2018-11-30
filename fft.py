import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from time import time as tt
import sounddevice as sd
from numpy import int16, frombuffer

m = 48
def that_func(y, n, t):
	yf = scipy.fftpack.fft(y)
	xf = np.arange(n)

	if 0:
		for i in reversed(range(len(yf) // 2 - m)):
			yf[i + m] = yf[i]
			yf[i] = 0

		for i in range(len(yf) // 2 + m, len(yf)):
			yf[i - m] = yf[i]
			yf[i] = 0

	if 1:
		for i in range(m, len(yf) // 2):
			yf[i - m] = yf[i]
			yf[i] = 0

		for i in reversed(range(len(yf) // 2, len(yf) - m)):
			yf[i + m] = yf[i]
			yf[i] = 0

	fig, ax = plt.subplots()
	ax.plot(xf, np.abs(yf.real), 'r')
	ax.plot(xf, -np.abs(yf.imag), 'b')


	yy = scipy.fftpack.ifft(yf)
	fig, ax = plt.subplots()
	ax.plot(xf, yy)

	return yy


N = 1136
T = 1.0
x = np.linspace(0.0, N*T, N)
y = np.cos(50 * 2.0*np.pi*x)
fig, ax = plt.subplots()
ax.plot(x, y)
yy = that_func(y, N, T)

def callback(out_data, frames, time, status):
	out_data[:] = np.asarray((yy.reshape(1136, 1)+1) * 1000, dtype=int16)


stream = sd.OutputStream(samplerate=44100, callback=callback, dtype=int16, channels=1)
stream.start()

plt.show()
input()