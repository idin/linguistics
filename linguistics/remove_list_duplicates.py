def remove_list_duplicates(l):
	used = []
	unique_list = [x for x in l if x not in used and (used.append(x) or True)]
	return unique_list