from DModule.pfuncs import rgbsum
from os import path
import pickle
import json


class SharedSettings:
	def __init__(self):
		# BASE
		self.skin_color = (0.7, 0.7, 0.7)
		self.irises_color = (0.7, 0, 0)
		self.lips_color = (1, 0, 0)
		self.brows_color = (0.2, 0.6, 0)

		# CALCULATED
		self.nose_sides_color = ()

	def as_string(self):
		o = [self.skin_color, self.irises_color, self.lips_color, self.brows_color, self.nose_sides_color]
		return json.dumps(o)

	@staticmethod
	def from_string(s):
		o = json.loads(s)
		new_ss = SharedSettings()

		new_ss.skin_color = o[0]
		new_ss.irises_color = o[1]
		new_ss.lips_color = o[2]
		new_ss.brows_color = o[3]
		new_ss.nose_sides_color = o[4]

		return new_ss


class AvatarSettings:
	def __init__(self):
		self.show_avatar = True
		self.face_width_k = 1.0
		self.face_height_k = 1.0
		self.ss = SharedSettings()

	def calculate_new_values(self):
		self.ss.nose_sides_color = rgbsum(self.ss.skin_color, (-0.1, -0.1, -0.1))

	@staticmethod
	def load():
		if path.isfile("avatar.settings"):
			try:
				return pickle.load(open("avatar.settings", "rb"))
			except Exception as e:
				print(e)
				return AvatarSettings()
		else:
			return AvatarSettings()

	def save(self):
		pickle.dump(self, open("avatar.settings", "wb"))


another_avatar_ss = SharedSettings()
avatar_settings = AvatarSettings.load()
avatar_settings.calculate_new_values()
