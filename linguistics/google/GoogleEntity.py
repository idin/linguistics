from .GoogleTokenSpan import GoogleTokenSpan
from .GoogleSentiment import GoogleSentiment


class GoogleMention(GoogleTokenSpan):
	def __init__(self, dictionary, document, entity):
		text = dictionary.pop('text')
		content = text.pop('content')
		begin = text.pop('begin_offset')
		end = begin + len(content)
		super().__init__(dictionary=dictionary, document=document, begin=begin, end=end)
		self._text = content
		self._index = None
		self._entity = entity

	@property
	def entity(self):
		"""
		:rtype: GoogleEntity
		"""
		return self._entity

	@property
	def id(self):
		return self.document.id, 'mention', self.entity._index, self._index

class GoogleEntity:
	def __init__(self, dictionary, document):
		self._dictionary = dictionary
		self._document = document
		self._name = self._dictionary.pop('name')
		self._type = self._dictionary.pop('type')
		self._metadata = self._dictionary.pop('metadata')
		self._wikipedia_url = self._metadata.pop('wikipedia_url', None)
		self._salience = self._dictionary.pop('salience')
		sentiment = self._dictionary.pop('sentiment')
		self._sentiment = GoogleSentiment(score=sentiment.pop('score'), magnitude=sentiment.pop('magnitude'))
		self._mentions = [
			GoogleMention(dictionary=mention, document=self.document, entity=self)
			for mention in self._dictionary.pop('mentions')
		]
		for index, mention in enumerate(self.mentions):
			mention._index = index
		self._index = None

	def graph_str(self):
		return f'{self.name}\n({str(self._type).replace("_", " ")})'

	@property
	def id(self):
		return self.document.id, 'entity', self._index

	def __str__(self):
		return f'{self.name} ({self._type})'

	def __repr__(self):
		return str(self)

	@property
	def document(self):
		"""
		:type: .GoogleDocument.GoogleDocument
		"""
		return self._document

	@property
	def mentions(self):
		"""
		:rtype: list[GoogleMention]
		"""
		return self._mentions

	@property
	def dictionary(self):
		"""
		:rtype: dict
		"""
		return self._dictionary

	@property
	def name(self):
		return self._name

	@property
	def type(self):
		return self._type

	@property
	def salience(self):
		return self._salience

	@property
	def sentiment(self):
		"""
		:rtype: GoogleSentiment
		"""
		return self._sentiment

	@property
	def metadata(self):
		"""
		:rtype: dict or NoneType
		"""
		return self._metadata

	@property
	def wikipedia_url(self):
		"""
		:rtype: str or NoneType
		"""
		return self._wikipedia_url

	@property
	def tokens(self):
		return [token for mention in self.mentions for token in mention.tokens]
