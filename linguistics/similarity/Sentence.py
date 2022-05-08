import re
from .Word import Word
from .get_sentence_similarity import get_sentence_similarity


def get_similarity_matrix(s1, s2, case_sensitivity=1, first_char_weight=0, method='jaro_winkler'):
	if not isinstance(s1, Sentence):
		s1 = Sentence(s1)
	if not isinstance(s2, Sentence):
		s2 = Sentence(s2)

	max_length = max(s1.length, s2.length)

	def get_similarity_by_index(i1, i2):
		try:
			return s1.words[i1].get_similarity(
				s2.words[i2], case_sensitivity=case_sensitivity, first_char_weight=first_char_weight, method=method
			)
		except:
			return 0

	return [
		[(i1, i2, get_similarity_by_index(i1, i2))
		 for i2 in range(max_length)]
		for i1 in range(max_length)
	]


def get_similar_pairs(s1, s2, case_sensitivity=1, first_char_weight=0, method='jaro_winkler'):
	similarity_matrix = get_similarity_matrix(
		s1, s2, case_sensitivity=case_sensitivity, first_char_weight=first_char_weight, method=method
	)

	flat_list = [e for l in similarity_matrix for e in l]
	sorted_similarities = sorted(flat_list, key=lambda x: -x[2])

	result = []
	for i1, i2, similarity in sorted_similarities:
		if similarity_matrix[i1][i2] is not None:
			if i1 < s1.length and i2 < s2.length:
				word_1, word_2 = s1.words[i1], s2.words[i2]
				index_1, index_2 = i1, i2
			elif i1 < s1.length:
				word_1, word_2 = s1.words[i1], None
				index_1, index_2 = i1, None
			else:
				word_1, word_2 = None, s2.words[i2]
				index_1, index_2 = None, i2

			result.append({
				'word_1': word_1, 'word_2': word_2, 'similarity': similarity,
				'index_1': index_1, 'index_2': index_2
			})

			# remove all elements at column i2 (iterate over rows)
			for j1 in range(len(similarity_matrix)):
				similarity_matrix[j1][i2] = None

			# remove all elements at row i1 (iterate over columns)
			for j2 in range(len(similarity_matrix[i1])):
				similarity_matrix[i1][j2] = None

	return result


class Sentence:
	def __init__(self, string):
		if isinstance(string, self.__class__):
			self._string = string._string
			self._words = string.words.copy()
		elif isinstance(string, (list, tuple)):
			self._words = [Word(x) for x in string]
			self._string = ' '.join([str(x) for x in string])
		else:
			self._string = str(string)
			self._words = None

	@property
	def words(self):
		if self._words is None:
			words = [
				Word(string=s)
				for s in re.findall(r'[^\s!,.?":;]+', self._string)
			]
			self._words = [word for word in words if word.length > 0]

		return self._words

	def __sub__(self, other):
		"""
		:type other: Sentence
		:rtype: float
		"""
		return (1-self.get_similarity(other))*max(self.length, other.length)

	def get_similarity(self, other, first_char_weight=0, first_word_weight=0, case_sensitivity=1, method='jaro_winkler'):
		"""
		:type other: Sentence
		:rtype: float
		"""
		return get_sentence_similarity(
			words1=self.words, words2=other.words,
			first_word_weight=first_word_weight, first_char_weight=first_char_weight,
			case_sensitivity=case_sensitivity, method=method
		)

	def get_similarity_matrix(self, other, first_char_weight=0, case_sensitivity=1, method='jaro_winkler'):
		return get_similarity_matrix(
			s1=self, s2=other, first_char_weight=first_char_weight, case_sensitivity=case_sensitivity, method=method
		)

	def get_similar_pairs(self, other, first_char_weight=0, case_sensitivity=1, method='jaro_winkler'):
		return get_similar_pairs(
			s1=self, s2=other, first_char_weight=first_char_weight, case_sensitivity=case_sensitivity, method=method
		)

	def get_unordered_similarity(
			self, other, first_char_weight=0, case_sensitivity=1, method='jaro_winkler', weights=None
	):
		"""
		:type other: Sentence or str or list[str] or list[Word]
		:type first_char_weight: int or float
		:type case_sensitivity: int or float
		:type method: str
		:type weights: NoneType or list[float]
		:rtype: float
		"""
		similarity_order = get_similar_pairs(
			s1=self, s2=other, first_char_weight=first_char_weight, case_sensitivity=case_sensitivity, method=method
		)

		if weights is None:
			return sum([x['similarity'] for x in similarity_order])/len(similarity_order)
		elif isinstance(weights, (list, tuple)):
			count = min([len(weights), len(similarity_order)])
			total = sum([similarity_order[i]['similarity'] * weights[i] for i in range(count)])
			total_weights = sum(weights[:count])
			return total / total_weights

	def __contains__(self, item):
		"""
		:type item: Word or str
		:rtype: bool
		"""
		return str(item) in self._words

	def get_initials(self):
		return [word.initial for word in self._words]

	def get_initial_intersection_score(self, other):
		"""
		:type other: Sentence
		:rtype: int
		"""
		return len(set(self.get_initials()).intersection(set(other.get_initials())))


	def get_word(self, i=1):
		try:
			return self.words[i-1].string
		except:
			return None

	@property
	def length(self):
		return len(self.words)

	def lower(self, inplace=False):
		if inplace:
			self._words = [w.lower(inplace=False) for w in self.words]
			self._string = self._string.lower()
		else:
			return self.__class__(string=self._string.lower())

	def remove_words(self, words, inplace=False):
		"""
		:type words: list of Word or list of str
		"""
		new_words = [w for w in self.words if w not in words]
		new_strings = [w.string for w in new_words]
		if inplace:
			self._words = new_words
			self._string = ' '.join(new_strings)
		else:
			return self.__class__(string=' '.join(new_strings))

	def replace_words(self, replacement_dict, inplace=False):
		"""
		:param replacement_dict: a dictionary with words to be replaced as keys and replacements as values
		:type replacement_dict: dict
		"""
		new_strings = [replacement_dict[w.string] if w.string in replacement_dict else w.string for w in self.words]
		if inplace:
			self._words = [Word(string) for string in new_strings]
			self._string = ' '.join(new_strings)
		else:
			return self.__class__(string=' '.join(new_strings))

	def __str__(self):
		return self._string

	def __repr__(self):
		words = self.words
		return ' '.join([str(word) for  word in words])