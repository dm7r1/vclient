import json


open_bracket = 123    # {
close_bracket = 125   # }


def bjson2object(barray):
	return json.loads(barray.decode())


def bjson2objects(barray):
	brackets = 0
	substrings = []
	last_idx = 0
	i = 0
	arr_len = len(barray)
	while i < arr_len:
		if barray[i] == 123:
			brackets += 1
		elif barray[i] == 125:
			brackets -= 1
			if brackets == 0:
				substrings.append((last_idx, i + 1))
				last_idx = i + 1
		i += 1
	for sub in substrings:
		yield json.loads(barray[sub[0]:sub[1]].decode())


def object2bjson(object):
	return json.dumps(object).encode()
