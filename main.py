import sys
from PySide.QtGui import *
from GUI.mainWindow import MainWindow
from superdata.us3r import user


def start_app(app):
	main_window = MainWindow()
	user.set_main_window(main_window)
	user.server.start()

	main_window.move(150, 200)
	main_window.show()

	app.exec_()
	user.server.stop_threads_and_close()
	sys.exit()
