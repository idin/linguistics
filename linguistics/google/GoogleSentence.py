from .GoogleTokenSpan import GoogleTokenSpan
from .GoogleSentiment import GoogleSentiment


class GoogleSentence(GoogleTokenSpan):
	def __init__(self, dictionary, document):

		text = dictionary.pop('text')
		content = text.pop('content')
		begin = text.pop('begin_offset')
		end = begin + len(content)

		super().__init__(dictionary=dictionary, document=document, begin=begin, end=end)

		self._text = content
		sentiment = self._dictionary.pop('sentiment')
		self._sentiment = GoogleSentiment(score=sentiment.pop('score'), magnitude=sentiment.pop('magnitude'))
		self._index = None

	@property
	def text(self):
		return self._text

	@property
	def id(self):
		return self.document.id, 'sentence', self._index

	@property
	def sentiment(self):
		"""
		:rtype: GoogleSentiment
		"""
		return self._sentiment

	def __str__(self):
		return self.text

	def __repr__(self):
		return str(self)





