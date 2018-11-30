# import cgl
import not_release.cgl_py as cgl
from PySide.QtOpenGL import *
from PySide.QtCore import *
from OpenGL.GL import *
import time
from threads.threads_storage import Threads
# from not_release.cgl_py import drawf
from superdata.us3r import user


qsrand(time.time())


class CanvasGL(QGLWidget):
	GL_MULTISAMPLE = 0x809D
	rot = 0.0

	def __init__(self, parent=None, width=800, height=500):
		super(CanvasGL, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
		self._polygons = []
		self.resize(width, height)
		self.server = user.server

	def create_and_star_recv_thread(self):
		Threads.set_recv_pts_thread(user.pconn_manager.make_pts_receive_thread(self))
		self.receive_thread = Threads.recv_pts_thread
		self.receive_thread.start()

	def showIt(self):
		user.main_window.right.call_button.setVisible(False)
		user.main_window.right.stop_button.setVisible(True)
		self.setVisible(True)

	def hideIt(self):
		self._polygons = []
		self.update()

	def initializeGL(self):
		pass

	def resizeGL(self, w, h):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-1., 1, -1., 1., -1., 1.)
		glViewport(0, 0, w, h)
		self.receive_thread.dmodel.set_w2h(h / w)

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT)
		glClearColor(1., 1., 1., 1.)

		cgl.drawf(self._polygons)

	def destroy(self, *args, **kwargs):
		self.receive_thread.off()

	def closeEvent(self, *args, **kwargs):
		self.receive_thread.off()

	def event(self, event):
		if event.type() == 999:
			self.hideIt()
		else:
			super(CanvasGL, self).event(event)
		return True
