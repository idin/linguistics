from itertools import zip_longest
import re
from .Word import Word
from .get_sentence_similarity import get_sentence_similarity

class Sentence:
	def __init__(self, string, similarity_function=None, word_similarity_function=None):
		self._string = str(string)
		if similarity_function is None:
			similarity_function = lambda words1, words2: get_sentence_similarity(
				words1=words1, words2=words2, first_char_weight=0.5, first_word_weight=1.0, case_sensitivity=0.1,
				method='sentence_jaro_winkler'
			)
		self._similarity_function = similarity_function
		self._word_similarity_function = word_similarity_function
		self._words = None


	@property
	def words(self):
		if self._words is None:
			words = [
				Word(string=s, similarity_function=self._word_similarity_function)
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

	def get_similarity(self, other):
		return self.get_similarity(other=other)

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
			return self.__class__(
				string=self._string.lower(), similarity_function=self._similarity_function,
				word_similarity_function=self._word_similarity_function
			)

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
			return self.__class__(string=' '.join(new_strings), similarity_function=self._similarity_function)


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
			return self.__class__(string=' '.join(new_strings), similarity_function=self._similarity_function)

	def __str__(self):
		return self._string

	def __repr__(self):
		words = self.words
		return ' '.join([str(word) for  word in words])