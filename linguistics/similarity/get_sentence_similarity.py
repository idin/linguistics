import numpy as np

from .get_string_similarity import get_string_similarity

def get_sentence_distance(words1, words2, first_char_weight=0, case_sensitivity=1, method='jaro_winkler'):
	"""
	:type words1: list[str] or str
	:type words2: list[str] or str
	:type first_char_weight: float
	:type case_sensitivity: float
	:type method: str
	:rtype: float
	"""
	if isinstance(words1, str):
		words1 = words1.split()
	elif not isinstance(words1, list):
		raise TypeError('words1 should either be a string or a list!')

	if isinstance(words2, str):
		words2 = words2.split()
	elif not isinstance(words2, list):
		raise TypeError('words2 should either be a string or a list')

	size_x = len(words1) + 1
	size_y = len(words2) + 1
	m = np.zeros((size_x, size_y))
	# create_matrix(h=size_x, w=size_y, obj=0)

	for i in range(size_x): m[i, 0] = i
	for j in range(size_y): m[0, j] = j
	for i in range(1, size_x):
		for j in range(1, size_y):
			w1 = words1[i - 1]
			w2 = words2[j - 1]
			normalized_distance = 1 - get_string_similarity(
				s1=w1, s2=w2, method=method,
				first_char_weight=first_char_weight,
				case_sensitivity=case_sensitivity
			)
			m[i][j] = min(
				m[i - 1, j - 1] + normalized_distance,
				m[i - 1, j] + 1,
				m[i, j - 1] + 1
			)

	return m[size_x - 1, size_y - 1]


def get_sentence_similarity(
		words1, words2, first_char_weight=0, first_word_weight=0, case_sensitivity=1, method='jaro_winkler'
):
	"""
	:type words1: list[str] or str
	:type words2: list[str] or str
	:type first_char_weight: float
	:type first_word_weight: float
	:type case_sensitivity: float
	:type method: str
	:rtype: float
	"""
	if isinstance(words1, str):
		words1 = words1.split()
	elif not isinstance(words1, list):
		raise TypeError('words1 should either be a string or a list!')

	if isinstance(words2, str):
		words2 = words2.split()
	elif not isinstance(words2, list):
		raise TypeError('words2 should either be a string or a list')

	distance = get_sentence_distance(
		words1=words1, words2=words2, method=method,
		case_sensitivity=case_sensitivity, first_char_weight=first_char_weight
	)
	if len(words1)==0 and len(words2)==0:
		return 1.0
	elif len(words1)==0 or len(words2)==0:
		return 0.0

	similarity = 1 - distance/max(len(words1), len(words2))

	if first_word_weight==0:
		return similarity
	elif first_word_weight<0:
		raise ValueError('first_word_weight cannot be negative!')
	else:
		first_word_similarity = get_string_similarity(
			s1=words1[0], s2=words2[0], method=method,
			case_sensitivity=case_sensitivity, first_char_weight=first_char_weight
		)
		return (similarity+first_word_similarity*first_word_weight)/(1+first_word_weight)

