def read_all(filename):
	string = ""
	with open(filename) as f:
		for line in f.readlines():
			string += line
	return string


def clear_layout(layout):
	while layout.count():
		item = layout.takeAt(0)
		if item.widget() is not None:
			item.widget().deleteLater()
		elif item.layout() is not None:
			clear_layout(item.layout())


def remove_layout(layout):
	clear_layout(layout)
	layout.deleteLater()
