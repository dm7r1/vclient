import sys
from cx_Freeze import setup, Executable


build_exe_options = {
	"include_msvcr": True,
	"include_files": [
		"superdata", "client", "client", "GUI", "resources", "threads", "utils",
		"not_release", "data", "DModule", ""],
	"packages": ["json", "numpy", "cv2", "dlib", "PySide", "imutils", "OpenGL", "sounddevice", "cffi", "socket", "Cryptodome"],
	"build_exe": "../client_build"}


base = None
if sys.platform == "win32":
	base = "Win32GUI"

setup(
	name="vchat",
	version="0.1",
	description="vector chat",
	options={"build_exe": build_exe_options},
	executables=[Executable("authorization.py", base=base)])
