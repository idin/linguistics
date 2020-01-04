from .levenshtein import get_levenshtein_similarity
from .jaro_winkler import get_jaro_winkler_similarity




def get_string_similarity(s1, s2, case_sensitivity=1.0, first_char_weight=0.0, method='jaro_winkler'):


	s1 = s1 or ''
	s2 = s2 or ''
	s1 = str(s1)
	s2 = str(s2)

	if method=='jaro_winkler':
		_get_similarity = get_jaro_winkler_similarity
	elif method=='levenshtein':
		_get_similarity = get_levenshtein_similarity
	else:
		raise ValueError(f'{method} is unknown!')

	if first_char_weight<0:
		raise ValueError('initial_weight cannot be negative!')

	if case_sensitivity==0:
		string_similarity = _get_similarity(s1, s2, case_sensitive=False)
		if first_char_weight>0 and len(s1)>0 and len(s2)>0:
			initials_equal = int(s1[0].lower() == s2[0].lower())
		else:
			initials_equal = 0
		similarity = (string_similarity + initials_equal * first_char_weight) / (1 + first_char_weight)

	elif case_sensitivity==1:
		string_similarity = _get_similarity(s1, s2, case_sensitive=True)
		if first_char_weight>0 and len(s1)>0 and len(s2)>0:
			initials_equal = int(s1[0] == s2[0])
		else:
			initials_equal = 0
		similarity = (string_similarity + initials_equal * first_char_weight) / (1 + first_char_weight)

	elif case_sensitivity>0 and case_sensitivity<1:
		sensitive = _get_similarity(s1, s2, case_sensitive=True)
		insensitive = _get_similarity(s1, s2, case_sensitive=False)
		string_similarity = case_sensitivity*sensitive + (1-case_sensitivity)*insensitive
		if first_char_weight>0 and len(s1)>0 and len(s2)>0:
			initials_equal = case_sensitivity*int(s1[0] == s2[0]) + (1-case_sensitivity)*int(s1[0].lower() == s2[0].lower())
		else:
			initials_equal = 0
		similarity = (string_similarity + initials_equal * first_char_weight) / (1 + first_char_weight)

	else:
		raise ValueError('case_sensitivity should be between 0 and 1.')

	return similarity
