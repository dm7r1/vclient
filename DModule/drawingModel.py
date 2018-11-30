from DModule.faceDModule import FaceDModule
from DModule.eyesDmodule import EyesDmodule
import numpy as np


class DrawingModel:
	def __init__(self, final_width, final_height):
		self._last_face_width = 100
		self._last_center_x = 150
		self._last_center_y = 150

		self._w2h = final_width / final_height
		self._face_dmodule = FaceDModule()
		self._eyes_dmodule = EyesDmodule()

	def set_w2h(self, w2h):
		self._w2h = w2h

	def process(self, source_points):
		if len(source_points) == 0:
			return []
		face_width = ((source_points[16, 0] - source_points[0, 0]) + self._last_face_width * 15) // 16
		self._last_face_width = face_width
		ky = (1 / face_width * -1) * 1.1
		kx = ky * self._w2h
		center_x = (source_points[33, 0] + self._last_center_x * 7) // 8
		center_y = (source_points[33, 1] + self._last_center_y * 7) // 8
		self._last_center_x, self._last_center_y = center_x, center_y
		delta_x, delta_y = - center_x * kx, - center_y * ky
		points = np.ndarray(shape=source_points.shape)
		for i in range(70):
			points[i, 0] = source_points[i, 0] * kx + delta_x  # 0.0025 sec
			points[i, 1] = source_points[i, 1] * ky + delta_y
		self._face_dmodule.calc_points(points)  # 0.001 sec
		self._eyes_dmodule.calc_points(points)  #

		polygon_xyc = list()

		polygon_xyc.extend(self._eyes_dmodule.get_polygons())  # 0.003 sec
		polygon_xyc.extend(self._face_dmodule.get_polygons())  #

		return polygon_xyc
