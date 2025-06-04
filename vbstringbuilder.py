
def dict_csv(keys: str,values: str) -> dict:
	"""
	Creates a dictionary from csv items.

	Arguments:
		keys: A VB string of keys.
		values: a string of values.

	Returns:
		A dictionary of the 2 arguments.
	"""
	a_dict: dict = {}
	if len(keys) != len(values):
		print(f"Number of items and prices are not equal")
		print(f"Key count: {len(keys)}")
		print(f"Value count: {len(values)}")
		return -1
	else:
		for i in range(len(keys)):
			a_dict.setdefault(keys[i].replace('"', '').strip(),values[i].replace('"', '').strip())
	return a_dict

def dict_line(keys: str,values: str) -> dict:
	"""
	Creates a dictionary from line items.

	Arguments:
		keys: a string that is formated with line returns.
		values: a string that is formated with line returns.
	Returns:
		a dictionary of key value pairs.
	"""
	new_dict: dict = {}
	if len(keys) != len(values):
		print(f"Number of items and prices are not equal")
		print(f"Key count: {len(keys)}")
		print(f"Value count: {len(values)}")
		return -1
	else:
		for i in range(len(keys)):
			new_dict.setdefault(keys[i].strip(),values[i].strip())
	return new_dict

def bna_data(a_dict: dict,b_dict: dict) -> str:
	"""
	Show the difference in vaules from a_dict and b_dict.

	Arguments:
		a_dict: The dictionary of the current key value pairs matched from the current strings.
		b_dict: The dictionary of the new key value pairs matches from the spreadsheet.
	Returns:
		A new line for each key and the value of a_dict and b_dict.
	"""
	bna_data: str = ""
	bna_data = '\n'.join(f"{i}: {a_dict.get(i)} -> {b_dict.get(i)}" for i in a_dict.keys())
	return bna_data

def remove_empties(a_dict: dict) -> tuple:
	"""
	Removes the empties from the a dictionary

	Arguments:
		a_dict: A dictionary that may or may not have empty values.
	Returns:
		a tuple of key value pairs and list of removed keys.
	"""
	keys_with_values_dict: dict = {}
	removed_keys: list = []
	for key in a_dict.keys():
		if a_dict.get(key) != '':
			keys_with_values_dict.setdefault(key,a_dict.get(key))
		else:
			removed_keys.append(f"Key: {key}")
	return keys_with_values_dict, removed_keys

def added_items(a_dict: dict,b_dict: dict) -> list:
	"""
	Creates a list of items added to the key values.

	Arguments:
		a_dict: Contains the list of items you are coming from.
		b_dict: Contains the list of items you are going to.
	Returns: 
		List of keys that were added.
	"""
	items_added: list = []
	for key in (set(list(b_dict.keys())) - set(list(a_dict.keys()))):
		items_added.append(f"Key: {key}")
	return items_added

def list_of_string(a_list: list) -> str:
	"""
	Creates a string from the list if items passed.

	Arguments:
		a_list: List of items to turn into a VB ListOfString
	Returns:
		The string returned is a csv formated string with each item surounded in double quotes. This returns a formatted VB ListOfString.	
	"""
	string = ','.join(['"'+i+'"' for i in list(a_list)])
	return string

def list_of_number(a_list):
	"""
	Creates a string from the list if items passed.

	Arguments:
		a_list: List of items to turn into a VB Int or Double
	Returms:
		The string returned is a csv formated string with each item. This is used for returning a list of intergers or doubles for VB.
	"""
	string = ','.join([i for i in list(a_list)])
	return string
