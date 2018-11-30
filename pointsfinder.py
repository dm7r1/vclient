import cv2
import imutils
import dlib
import math
import numpy as np
from imutils import face_utils


class PointsFinder:
	def __init__(self, img_width=350):
		self._haar = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
		self._predictor = dlib.shape_predictor("data/predictorFace.dat")
		self._img_gray = 0
		self._img_width = img_width
		self._shape = list()

	def open_cam(self):
		self._cap = cv2.VideoCapture(0)

	def _find_pupils(self):
		try:
			pupils = list()
			eye_rects = (	(self._shape[36][0], min(self._shape[37][1], self._shape[38][1]),  # x1 y1  0
							self._shape[39][0], max(self._shape[40][1], self._shape[41][1])),  # x2 y2  0
							(self._shape[42][0], min(self._shape[43][1], self._shape[44][1]),  # x1 y1  1
							self._shape[45][0], max(self._shape[47][1], self._shape[46][1])))  # x2 y2  1

			for x1, y1, x2, y2 in eye_rects:
				eye_img = self._img_gray[y1:y2, x1:x2]

				pupil = [0, 0]
				weight = 0
				for y in range(eye_img.shape[0]):
					for x in range(eye_img.shape[1]):
						c = 255 - int(eye_img[y, x])
						w = int(math.pow(c, 10) // math.pow(64, 9))  # TODO - fix it
						pupil[0] += x * w
						pupil[1] += y * w
						weight += w

				pupil[0] = x1 + pupil[0] // weight
				pupil[1] = y1 + pupil[1] // weight
				pupils.append(tuple(pupil))
			return pupils
		except Exception:
			return [[0, 0], [0, 0]]

	@property
	def img_width(self):
		return self._img_width

	def get_points(self):
		if not self._cap.isOpened():
			return tuple()
		try:
			r, img = self._cap.read()
			self._img_gray = cv2.cvtColor(imutils.resize(img, width=self._img_width), cv2.COLOR_BGR2GRAY)

			faces = self._haar.detectMultiScale(self._img_gray, 1.3, 5)
			if len(faces) == 0:
				return tuple()
			x, y, w, h = faces[0]

			face_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

			self._shape = self._predictor(self._img_gray, face_rect)

			self._shape = face_utils.shape_to_np(self._shape)
			pupils = self._find_pupils()

			self._shape = np.append(self._shape, pupils, axis=0)
			return self._shape
		except Exception:
			return tuple()

	def release_cam(self):
		if hasattr(self, "_cap") and self._cap.isOpened():
			self._cap.release()
