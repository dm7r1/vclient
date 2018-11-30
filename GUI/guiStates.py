class GUIStates:
	NO_CONTACT = -1

	contact_id = NO_CONTACT

	@staticmethod
	def set_user(user):
		GUIStates.user = user

	@staticmethod
	def set_widgets(right):
		GUIStates.right = right

	@staticmethod
	def set_contact_id(uid):
		GUIStates.contact_id = uid
		GUIStates.right.post_set_contact()

	@staticmethod
	def get_contact_id():
		return GUIStates.contact_id

	@staticmethod
	def set_no_contact():
		GUIStates.contact_id = GUIStates.NO_CONTACT
