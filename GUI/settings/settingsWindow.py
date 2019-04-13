from PySide.QtGui import QMainWindow, QLabel, QWidget, QColorDialog, QColor, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, QSlider
import PySide.QtCore
from avatar_settings import avatar_settings
from superdata.us3r import user

import sounddevice as sd


class SettingsWindow(QMainWindow):
	def __init__(self):
		super(SettingsWindow, self).__init__()
		self.setWindowTitle("Settings")
		self.setFixedSize(400, 400)

		main_layout = QVBoxLayout()

		self.qcd_skin = QColorDialog()
		self.qcd_skin.colorSelected.connect(self.set_skin_color)
		self.qcd_skin_btn = QPushButton("change skin color")
		self.qcd_skin_btn.clicked.connect(self.qcd_skin.show)
		main_layout.addWidget(self.qcd_skin_btn)

		self.qcd_irises = QColorDialog()
		self.qcd_irises.colorSelected.connect(self.set_irises_color)
		self.qcd_irises_btn = QPushButton("change irises color")
		self.qcd_irises_btn.clicked.connect(self.qcd_irises.show)
		main_layout.addWidget(self.qcd_irises_btn)

		self.qcd_brows = QColorDialog()
		self.qcd_brows.colorSelected.connect(self.set_brows_color)
		self.qcd_brows_btn = QPushButton("change brows color")
		self.qcd_brows_btn.clicked.connect(self.qcd_brows.show)
		main_layout.addWidget(self.qcd_brows_btn)

		self.qcd_lips = QColorDialog()
		self.qcd_lips.colorSelected.connect(self.set_lips_color)
		self.qcd_lips_btn = QPushButton("change lips color")
		self.qcd_lips_btn.clicked.connect(self.qcd_lips.show)
		main_layout.addWidget(self.qcd_lips_btn)

		self.qs_face_width_k = QSlider(PySide.QtCore.Qt.Orientation.Horizontal)
		self.qs_face_width_k.setMinimum(50)
		self.qs_face_width_k.setMaximum(180)
		self.qs_face_width_k.setValue(avatar_settings.face_width_k * 100)
		self.qs_face_width_k.valueChanged.connect(self.set_face_width_k)
		main_layout.addWidget(QLabel("face width k"))
		main_layout.addWidget(self.qs_face_width_k)

		self.qs_face_height_k = QSlider(PySide.QtCore.Qt.Orientation.Horizontal)
		self.qs_face_height_k.setMinimum(50)
		self.qs_face_height_k.setMaximum(180)
		self.qs_face_height_k.setValue(avatar_settings.face_height_k * 100)
		self.qs_face_height_k.valueChanged.connect(self.set_face_height_k)
		main_layout.addWidget(QLabel("face height k"))
		main_layout.addWidget(self.qs_face_height_k)

		self.qcheck_show_avatar = QCheckBox()
		self.qcheck_show_avatar.setChecked(avatar_settings.show_avatar)
		self.qcheck_show_avatar.stateChanged.connect(self.set_show_avatar)
		show_avatar_layout = QHBoxLayout()
		show_avatar_layout.addWidget(self.qcheck_show_avatar)
		show_avatar_layout.addWidget(QLabel("show avatar"))
		main_layout.addLayout(show_avatar_layout)

		self.setCentralWidget(QWidget())
		self.centralWidget().setLayout(main_layout)

	def apply_changes(self):
		avatar_settings.calculate_new_values()
		user.server.send_face_ss(avatar_settings.ss.as_string())
		avatar_settings.save()

	def set_face_width_k(self):
		avatar_settings.face_width_k = self.qs_face_width_k.value() / 100
		self.apply_changes()

	def set_face_height_k(self):
		avatar_settings.face_height_k = self.qs_face_height_k.value() / 100
		self.apply_changes()

	def set_show_avatar(self):
		avatar_settings.show_avatar = self.qcheck_show_avatar.isChecked()
		self.apply_changes()

	def set_skin_color(self):
		avatar_settings.ss.skin_color = self.qcd_skin.selectedColor().getRgbF()[:3]
		self.apply_changes()

	def set_irises_color(self):
		avatar_settings.ss.irises_color = self.qcd_irises.selectedColor().getRgbF()[:3]
		self.apply_changes()

	def set_brows_color(self):
		avatar_settings.ss.brows_color = self.qcd_brows.selectedColor().getRgbF()[:3]
		self.apply_changes()

	def set_lips_color(self):
		avatar_settings.ss.lips_color = self.qcd_lips.selectedColor().getRgbF()[:3]
		self.apply_changes()

	def showEvent(self, *args, **kwargs):
		pass