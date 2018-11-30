from OpenGL.GL import glBegin, GL_POLYGON, glColor3f, glVertex2f, glEnd, glFlush


def drawf(polys):
	glBegin(GL_POLYGON)
	glColor3f(1, 1, 1)
	glVertex2f(-1, -1)
	glVertex2f(1, -1)
	glVertex2f(1, 1)
	glVertex2f(-1, 1)
	glEnd()

	for xyc in polys:
		color = xyc[len(xyc) - 1]
		glColor3f(color[0], color[1], color[2])
		glBegin(GL_POLYGON)
		i = 0
		xyc_len = len(xyc) - 1
		while i < xyc_len:
			glVertex2f(xyc[i][0], xyc[i][1])
			i += 1
		glEnd()
	glFlush()
