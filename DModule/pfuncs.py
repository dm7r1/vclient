import math


def to01(clr):
	for i in range(3):
		if clr[i] < 0:
			clr[i] = 0
		elif clr[i] > 1:
			clr[i] = 1


def light(r, g, b, x, y):  # TODO FIX
	d = math.sqrt((x - 200) ** 2 + (y - 200) ** 2)
	d = int(d // 15 * 3)
	clr = [r - d, g - d, b - d]
	to01(clr)
	return clr


def shine(clr, a):
	r, g, b = clr
	a = (4 - a % 4) / 8 + 0.5
	clr = [r * a, g * a, b * a]
	return clr


def dist(p1, p2):
	return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def tg(p1, p2):
	return (p1[0] - p2[0]) / (p1[1] - p2[1])


def cos(p1, p2):
	a = p1[0] - p2[0]
	b = p1[1] - p2[1]
	return a / math.sqrt(a * a + b * b)


def sin(p1, p2):
	cosa = cos(p1, p2)
	return math.sqrt(1. - cosa * cosa)


def to_co(sin):
	return math.sqrt(1 - sin * sin)


def mul(p, s):
	return p[0] * s, p[1] * s


def delta(p1, p2):
	return p1[0] - p2[0], p1[1] - p2[1]


def psum(p1, p2):
	return p1[0] + p2[0], p1[1] + p2[1]


def med(*points):
	x = 0
	y = 0
	i = 0
	for p in points:
		i += 1
		x += p[0]
		y += p[1]
	return x / i, y / i


def medk(p1, p2, k1, k2):
	return p1[0] * k1 + p2[0] * k2, p1[1] * k1 + p2[1] * k2