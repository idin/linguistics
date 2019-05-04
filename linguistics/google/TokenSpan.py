from .DocumentObject import DocumentObject
from .Token import Token


class TokenSpan(DocumentObject):
	def __init__(self, dictionary, document, begin, end):
		super().__init__(dictionary=dictionary, document=document, begin=begin, end=end)
		self._tokens = None

	def __str__(self):
		return ', '.join([str(token) for token in self.tokens])

	def __repr__(self):
		return str(self)

	@property
	def tokens(self):
		"""
		:rtype: list[Token]
		"""
		if self._tokens is None:
			self._tokens = [
				token for token in self.document.tokens if token.begin >= self.begin and token.end <= self.end
			]
		return self._tokens
