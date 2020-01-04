from editdistance import eval as _get_levenshtein_distance


def get_levenshtein_distance(s1, s2, case_sensitive=True):
	if not case_sensitive:
		s1 = s1.lower()
		s2 = s2.lower()
	return _get_levenshtein_distance(s1, s2)


def get_levenshtein_similarity(s1, s2, case_sensitive=True):
	return 1-get_levenshtein_distance(s1, s2, case_sensitive=case_sensitive)/max(len(s1), len(s2))

