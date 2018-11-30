from tkinter import *
from DModule.faceDModule import FaceDModule
from pointsfinder import PointsFinder
from random import randint
import cv2

clrs = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')


def clr(r, g, b):
	return '#' + clrs[r // 16] + clrs[r % 16] + clrs[g // 16] + clrs[g % 16] + clrs[b // 16] + clrs[b % 16]


def trans_x(x):
	return (x - 150) * 3.5


def trans_y(y):
	return (y - 72) * 3.5


def trans_p(x, y):
	return trans_x(x) + 350, trans_x(y)

pf = PointsFinder()
pf.open_cam()

face_points2 = pf.get_points()
pf.release_cam()
root = Tk()

canvas = Canvas(root, width=500, height=500)

# face = FaceDModule()
# face.calc_points(face_points2)

canvas.delete("all")

im = cv2.imread("D:/resources/zuckerberg.jpg")

# for xyc in face.get_polygons():
# 	r, g, b = randint(120, 180), randint(120, 180), randint(120, 188)
# 	color = xyc.pop()
# 	points = []
# 	j = 0
# 	for pnt in xyc:
# 		pnt = trans_p(*pnt)
# 		points.append(pnt[0])
# 		points.append([pnt[1]])
# 		j += 1
# 	canvas.create_polygon(points, fill=clr(r, g, b))
import imutils
im = imutils.resize(im, width=700)
cv2.rectangle(im, (0, 0), (1000, 1000), (0, 0, 0), 1000)
for p in face_points2:
	x, y = p
	x = x * 7 - 1020
	y = y * 7 - 200
	cv2.circle(im, (x, y), 3, (255, 255, 255), 1)

cv2.imshow("SUCK", im)
cv2.waitKey(0)
i = 0
for point in face.T_get_pts():
	canvas.create_text(*trans_p(*point), text=str(i))
	i += 1

canvas.pack()

root.mainloop()