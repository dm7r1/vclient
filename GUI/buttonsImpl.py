from .buttons import CircleButton, TextButton
from .removeFriendWindow import RemoveFriendWindow
from .guiStates import GUIStates
from .settings.settingsWindow import SettingsWindow
from superdata.us3r import user


class AcceptButton(TextButton):
	def __init__(self, uid, parent_box):
		def call_func():
			user.accept(uid)
			parent_box.remove_me()

		super(AcceptButton, self).__init__(call_func, "accept")
		self.label.setObjectName("AcceptButton")


class RefuseButton(TextButton):
	def __init__(self, uid, parent_box):
		def refuse_func():
			user.refuse(uid)
			parent_box.remove_me()

		super(RefuseButton, self).__init__(refuse_func, "refuse")
		self.label.setObjectName("RefuseButton")


class StopButton(CircleButton):
	def __init__(self):
		def stop_call_func():
			if user.pconn_manager.is_calling:
				user.stop_req()
			else:
				user.stop_call()
			GUIStates.set_contact_id(GUIStates.get_contact_id())
			self.setVisible(False)

		super(StopButton, self).__init__(
			stop_call_func, text="stop", css_label_name="RedTextButton")


class CallButton(CircleButton):
	def __init__(self):
		def call_func():
			user.call(GUIStates.get_contact_id())
			user.main_window.right.canvas.showIt()
			user.main_window.right.remove_button.setVisible(False)

		super(CallButton, self).__init__(
			call_func, text="call", css_label_name="GreenTextButton")


class RemoveButton(TextButton):
	def __init__(self):
		def remove_friend_func():
			uid = GUIStates.get_contact_id()
			if uid != -1 and user.get_contact(uid):
				self.removeWin = RemoveFriendWindow(uid)
				self.removeWin.show()

		super(RemoveButton, self).__init__(remove_friend_func, "remove")
		self.label.setObjectName("RemoveTextButton")


class SettingsButton(TextButton):
	def __init__(self):
		self.settings_window = SettingsWindow()

		def open_setting_func():
			self.settings_window.show()

		super(SettingsButton, self).__init__(open_setting_func, "settings")
