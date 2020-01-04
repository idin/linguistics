
import re
from .get_string_similarity import get_string_similarity


class Word:
	def __init__(self, string, similarity_function=None):
		if string is None: string = ''
		if type(string) is Word:
			string = string._string
		else:
			string = str(string)
		self._string = re.sub(r'\W+', '', string)

		if similarity_function is None:
			similarity_function = lambda s1, s2: get_string_similarity(
				s1=s1, s2=s2, case_sensitivity=0.1, first_char_weight=0.5, method='jaro_winkler'
			)
		self._similarity_function = similarity_function

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

		try:
			result = self._similarity_function(self.string, str(other))
		except:
			print(f'{self}, {other}')
			raise
		return result

	def get_similarity(self, other):
		if other is None: return 0
		return self._similarity_function(self.string, str(other))

	def __eq__(self, other):
		return self.string == str(other)

	def lower(self, inplace=False):
		if inplace:
			self._string = self.string.lower()
		else:
			return self.__class__(string=self.string.lower(), similarity_function=self._similarity_function)

	def __repr__(self):
		return self._string

	def __str__(self):
		return self._string

