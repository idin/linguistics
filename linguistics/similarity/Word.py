import re
from .get_string_similarity import get_string_similarity


class Word:
	def __init__(self, string):
		if string is None: string = ''
		if isinstance(string, self.__class__):
			string = string._string
		else:
			string = str(string)
		self._string = re.sub(r'\W+', '', string)

	@property
	def string(self):
		return self._string

	@property
	def initial(self):
		return self.string[0].upper()

	@property
	def length(self):
		return len(self._string)

	def __sub__(self, other):
		"""
		:type other: Word
		:rtype: float
		"""
		return self.get_similarity(other=other)

	def get_similarity(self, other, case_sensitivity=1.0, first_char_weight=0.0, method='jaro_winkler'):
		if other is None:
			return 0
		else:
			return get_string_similarity(
				s1=self.string, s2=other.string, method=method,
				case_sensitivity=case_sensitivity, first_char_weight=first_char_weight
			)

	def __eq__(self, other):
		return self.string == str(other)

	def lower(self, inplace=False):
		if inplace:
			self._string = self.string.lower()
		else:
			return self.__class__(string=self.string.lower())

	def __repr__(self):
		return self._string

	def __str__(self):
		return self._string

