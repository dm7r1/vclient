from DModule.pfuncs import *
import avatar_settings


class FaceDModule:
	_pts = ()

	def calc_points(self, pts):
		self._pts = pts

		# cos_a = cos(pts[33], pts[27])
		# sin_a = to_co(cos_a)
		# dp = np.array((cos_a, sin_a)) * -70
		# p = pts[0] + dp
		# pts[70] = p  # 70
		# p = psum(pts[16], dp)
		# pts[71] = p  # 71 # TODO remove 70 and 71 points
		p = (pts[31] + pts[30]) / 2
		p = p + p - pts[32]
		pts[72] = p  # 72
		p = (pts[35] + pts[30]) / 2
		p = p + p - pts[34]
		pts[73] = p  # 73
		v30_72 = pts[72] - pts[30]
		v30_73 = pts[73] - pts[30]
		pts[74] = pts[29] + v30_72 * 0.8  # 74
		pts[75] = pts[29] + v30_73 * 0.8  # 75
		pts[76] = pts[28] + v30_72  # 76
		pts[77] = pts[28] + v30_73  # 77
		pts[78] = (pts[3] + pts[4] + pts[31] + pts[48]) / 4  # 78
		pts[79] = (pts[13] + pts[12] + pts[35] + pts[54]) / 4  # 79
		pts[80] = (pts[3] + pts[31] + pts[76] + pts[1]) / 4  # 80
		pts[81] = (pts[13] + pts[35] + pts[77] + pts[15]) / 4  # 81
		pts[82] = (pts[28] + pts[80] + pts[0]) / 3  # 82
		pts[83] = (pts[28] + pts[81] + pts[16]) / 3  # 83
		pts[84] = (pts[7] + pts[8] + pts[9] + pts[57]) / 4  # 84
		pts[85] = pts[77] * 0.9 + pts[83] * 0.1  # 85
		pts[86] = pts[76] * 0.9 + pts[82] * 0.1  # 86
		pts[87] = pts[75] * 0.9 + pts[83] * 0.1  # 87
		pts[88] = pts[74] * 0.9 + pts[82] * 0.1  # 88
		pts[89] = pts[73] * 0.9 + pts[81] * 0.1  # 89
		pts[90] = pts[72] * 0.9 + pts[80] * 0.1  # 90
		pts[91] = pts[33] * 0.9 + pts[30] * 0.1  # 91
		pts[92] = (0, 0)  # 92                             FREE POINT !!!
		# 3rd POINTS IN OUTER TRIANGLES
		pts[93] = (pts[9] + pts[10] + pts[56]) / 3  # 93
		pts[94] = (pts[6] + pts[7] + pts[58]) / 3  # 94
		pts[95] = (pts[10] + pts[11] + pts[55]) / 3  # 95
		pts[96] = (pts[5] + pts[6] + pts[59]) / 3  # 96
		pts[97] = (pts[11] + pts[12] + pts[54]) / 3  # 97
		pts[98] = (pts[4] + pts[5] + pts[48]) / 3  # 98
		pts[99] = (pts[12] + pts[13] + pts[79]) / 3  # 99
		pts[100] = (pts[3] + pts[4] + pts[78]) / 3  # 100
		pts[101] = (pts[13] + pts[14] + pts[81]) / 3  # 101
		pts[102] = (pts[2] + pts[3] + pts[80]) / 3  # 102
		pts[103] = pts[15] * 0.7 + pts[83] * 0.3  # 103
		pts[104] = pts[1] * 0.7 + pts[82] * 0.3  # 104

		# BROWS BOTTOM POINTS
		pts[105] = pts[26] * 0.8 + pts[45] * 0.2  # 105
		pts[106] = pts[17] * 0.8 + pts[36] * 0.2  # 106
		pts[107] = pts[25] * 0.8 + pts[44] * 0.2  # 107
		pts[108] = pts[18] * 0.8 + pts[37] * 0.2  # 108
		pts[109] = pts[24] * 0.8 + pts[43] * 0.2  # 109
		pts[110] = pts[19] * 0.8 + pts[38] * 0.2  # 110
		pts[111] = pts[23] * 0.8 + pts[43] * 0.2  # 111
		pts[112] = pts[20] * 0.8 + pts[38] * 0.2  # 112
		pts[113] = pts[22] * 0.8 + pts[42] * 0.2  # 113
		pts[114] = pts[21] * 0.8 + pts[39] * 0.2  # 114

	# TODO TEST METHOD
	def T_get_pts(self):
		return self._pts

	def light(self, clr, x, y):
		r, g, b = clr
		d = math.sqrt((x - 0) ** 2 + (y - 0.5) ** 2)
		d = d * 0.35
		clr = [r - d, g - d, b - d]
		to01(clr)
		return clr

	def get_polygons(self):
		polygon_xyc = list()
		j = 0
		for polygons_set, color in (
				(self._face_polygons, avatar_settings.another_avatar_ss.skin_color),
				(self._nose_sides_polygons, avatar_settings.another_avatar_ss.nose_sides_color),
				(self._lips_polygons, avatar_settings.another_avatar_ss.lips_color),
				(self._brows_polygons, avatar_settings.another_avatar_ss.brows_color),
				(self._black_polygons, (0, 0, 0)),
		):
			for polygon in polygons_set:
				j += 1
				line = []
				x, y, c = 0, 0, 0
				for i in polygon:
					x += self._pts[i][0]
					y += self._pts[i][1]
					c += 1
					line.append((self._pts[i][0], self._pts[i][1]))
				line.append(self.light(color, x / c, y / c))  # 134
				polygon_xyc.append(line)
		return polygon_xyc

	_face_polygons = (
		# FACE
		(48, 78, 31, 49),  # SIDES AROUND UNDER NOSE
		(54, 79, 35, 53),
		(32, 31, 49),  # UNDER NOSE order = (OUT -> IN) {
		(34, 35, 53),
		(32, 50, 49),
		(34, 52, 53),
		(32, 50, 51, 33),
		(34, 52, 51, 33),  # } UNDER NOSE
		(80, 31, 90, 88),
		(81, 35, 89, 87),
		(82, 80, 88),
		(83, 81, 87),
		(82, 88, 86),
		(83, 85, 87),
		(82, 39, 40, 41),
		(83, 42, 47, 46),
		(82, 39, 86),
		(83, 42, 85),
		# UNDER BROWS
		(36, 0, 17),
		(45, 16, 26),
		(36, 17, 18, 37),
		(45, 26, 25, 44),
		(18, 37, 38, 20, 19),
		(25, 44, 43, 23, 24),
		(38, 39, 21, 20),
		(43, 42, 22, 23),
		# NOSE
		(21, 27, 39),
		(22, 27, 42),
		(21, 27, 22),
		(76, 28, 27, 39),
		(77, 28, 27, 42),
		(76, 28, 29, 74),
		(77, 28, 29, 75),
		(72, 30, 29, 74),
		(73, 30, 29, 75),
		(31, 30, 72),
		(35, 30, 73),
		(31, 91, 30),
		(35, 91, 30),
		# OUTER SIDE TRIANGLES
		(9, 10, 93),
		(6, 7, 94),
		(10, 11, 95),
		(5, 6, 96),
		(11, 12, 97),
		(4, 5, 98),
		(12, 13, 99),
		(3, 4, 100),
		(13, 14, 101),
		(2, 3, 102),
		(14, 15, 16, 103),
		(0, 1, 2, 104),
		# OLD TOP INNER SIDE TRIANGLES
		(82, 104, 0),
		(83, 103, 16),
		(7, 8, 9, 84),
		# 2 OLD TOP TRIANGLES
		(82, 0, 36, 41),
		(83, 16, 45, 46),
		# SIDE IN
		(84, 94, 7),
		(84, 93, 9),
		(94, 96, 6),
		(93, 95, 10),
		(98, 96, 5),
		(97, 95, 11),
		(98, 100, 4),
		(97, 99, 12),
		(100, 102, 3),
		(99, 101, 13),
		(104, 102, 2),
		(103, 101, 14),
		# SIDE IN IN
		(84, 94, 57),
		(84, 93, 57),
		(94, 96, 59),
		(93, 95, 55),
		(94, 59, 58),
		(93, 55, 56),
		(94, 57, 58),
		(93, 57, 56),
		(98, 96, 48),
		(97, 95, 54),
		(96, 48, 59),
		(95, 54, 55),
		(98, 100, 78),
		(97, 99, 79),
		(98, 78, 48),
		(97, 79, 54),
		(104, 102, 82),
		(103, 101, 81),
		(102, 82, 80),
		(103, 83, 81),
		# VERY IN {
		(79, 81, 35),
		(78, 80, 31),
		# }
		(79, 81, 99),
		(78, 80, 100),
		(101, 99, 81),
		(102, 100, 80),
	)
	_brows_polygons = {
		# (26, 25, 105),  # 1st triangle
		# (17, 18, 106),  # 1st triangle
		(25, 105, 107),
		(18, 106, 108),

		(25, 24, 107),
		(18, 19, 108),
		(24, 107, 109),
		(19, 108, 110),

		(24, 23, 109),
		(19, 20, 110),
		(23, 109, 111),
		(20, 110, 112),

		(23, 22, 111),
		(20, 21, 112),
		# (22, 111, 113),  # lost triangle
		# (21, 112, 114),  # lost triangle
	}
	_nose_sides_polygons = (
		(77, 85, 42),
		(76, 86, 39),
		(77, 75, 87, 85),
		(76, 74, 88, 86),
		(75, 73, 89, 87),
		(74, 72, 90, 88),
		(73, 35, 89),
		(72, 31, 90),
		# nose bottom shadows
		(31, 91, 33, 32),
		(35, 91, 33, 34),
	)
	#  TODO FIX OVERLAP

	_lips_polygons = (
		# top lip
		(62, 51, 50),
		(62, 51, 52),
		(62, 61, 50),
		(62, 63, 52),
		(49, 61, 50),
		(53, 63, 52),
		(49, 61, 60),
		(53, 63, 64),
		(49, 60, 48),
		(53, 64, 54),
		# bottom lip
		(66, 57, 67),
		(66, 57, 65),
		(58, 57, 67),
		(56, 57, 65),
		(58, 60, 67),
		(56, 64, 65),
		(58, 60, 59),
		(56, 64, 55),
		(48, 60, 59),
		(54, 64, 55),
	)

	_black_polygons = (
		# mouth
		(60, 61, 62, 63, 64, 65, 66, 67),
	)
