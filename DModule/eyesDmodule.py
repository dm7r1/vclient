from DModule.pfuncs import *
import numpy as np
from math import sin as msin, cos as mcos, pi, sqrt
from DModule.pfuncs import dist
from avatar_settings import another_avatar_ss


class EyesDmodule:
	_pts = []

	def __init__(self):
		self._pupil_rgb = 0, 0, 0
		self._vertexes = 10
		s, c = msin(pi / self._vertexes * 2), mcos(pi / self._vertexes * 2)
		self._rotate_matrix = np.array(((c, s), (-s, c)))
		self._iris_k = 0.04
		self._pupil_k = 0.3
		self._eyes_pts = np.ndarray(shape=(2, 2, 72, 2), dtype=np.float32)

	def calc_points(self, pts):
		eye_height = pts[40, 1] - pts[37, 1]
		self._pts = pts
		pts[68] = pts[68] + (0, 0.3 * eye_height)
		pts[69] = pts[69] + (0, 0.3 * eye_height)
		l = sqrt(dist(self._pts[17], self._pts[26])) * self._iris_k
		iris_v = (0, l)

		for e in range(2):
			for i in range(self._vertexes):
				iris_v = np.dot(iris_v, self._rotate_matrix)
				self._eyes_pts[e, 0, i] = pts[68 + e] + iris_v
				self._eyes_pts[e, 1, i] = pts[68 + e] + iris_v * self._pupil_k

	def get_polygons(self):
		polygon_xyc = list()

		for pset in (range(36, 42),  range(42, 48)):
			line = []
			for p in pset:
				line.append((self._pts[p][0], self._pts[p][1]))
			line.append((1, 1, 1))
			polygon_xyc.append(line)

		for e in range(2):
			line_pupil = list()
			for i in range(self._vertexes):

				line_pupil.append((self._eyes_pts[e, 1, i, 0], self._eyes_pts[e, 1, i, 1]))  # xy

				line_iris = list()

				if i == self._vertexes - 1:
					ip1 = 0
				else:
					ip1 = i + 1

				line_iris.append((self._eyes_pts[e, 0, i, 0], self._eyes_pts[e, 0, i, 1]))  # xy
				line_iris.append((self._eyes_pts[e, 0, ip1, 0], self._eyes_pts[e, 0, ip1, 1]))  # xy
				line_iris.append((self._eyes_pts[e, 1, ip1, 0], self._eyes_pts[e, 1, ip1, 1]))  # xy
				line_iris.append((self._eyes_pts[e, 1, i, 0], self._eyes_pts[e, 1, i, 1]))  # xy
				line_iris.append(
					shine(
						another_avatar_ss.irises_color, i % 16
					)
				)
				polygon_xyc.append(line_iris)
			line_pupil.append(self._pupil_rgb)
			polygon_xyc.append(line_pupil)

		return polygon_xyc

