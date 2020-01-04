from abstract import Graph
from abstract.graph_style import NodeStyle

from .GoogleToken import GoogleToken
from .GoogleEntity import GoogleEntity
from .GoogleSentence import GoogleSentence
from .GoogleSentiment import GoogleSentiment


class GoogleDocument:
	def __init__(self, text=None, cloud=None, id=0, _analysis=None):
		"""
		:param str or NoneType text: a text to be converted to a GoogleDocument
		:param .GoogleCloud.GoogleCloud cloud: GoogleCloud API
		:param int or str id:
		:param dict or NoneType _analysis: result of GoogleCloud.analyze(text)
		"""

		if isinstance(text, list):
			text = ' '.join([str(x) for x in text])
		self._id = id

		if text is None and _analysis is None:
			raise ValueError('Either text or _analysis should be given!')
		elif text is None:
			self._dictionary = _analysis.copy()
			self._cloud = cloud
		elif _analysis is None:
			self._cloud = cloud
			self._dictionary = self._cloud.analyze(text=text)

		self._text = self._dictionary.pop('text')
		self._sentences = None
		self._tokens = None
		self._entities = None
		sentiment = self._dictionary.pop('document_sentiment')
		self._sentiment = GoogleSentiment(score=sentiment.pop('score'), magnitude=sentiment.pop('magnitude'))
		self._language = None
		self._graph = None

	def __str__(self):
		return '\n'.join([str(sentence) for sentence in self.sentences])

	def __repr__(self):
		return str(self)

	@property
	def id(self):
		return self._id

	@property
	def cloud(self):
		"""
		:rtype: .GoogleCloud.GoogleCloud
		"""
		return self._cloud

	def _get_from_dictionary(self, name):
		if name in self._dictionary:
			return self._dictionary.pop(name)
		elif name in ['text', 'sentiment', 'language']:
			return False
		else:
			return []

	def tokenize(self):
		self._text = self._get_from_dictionary('text')

		self._sentences = [GoogleSentence(x, document=self) for x in self._get_from_dictionary('sentences')]
		self._sentences.sort()
		for index, sentence in enumerate(self._sentences):
			sentence._index = index

		self._tokens = [GoogleToken(x, document=self) for x in self._get_from_dictionary('tokens')]
		self._tokens.sort()
		for index, token in enumerate(self._tokens):
			token._index = index

		self._entities = [GoogleEntity(x, document=self) for x in self._get_from_dictionary('entities')]
		for index, entity in enumerate(self._entities):
			entity._index = index

		self._sentiment = self._get_from_dictionary('sentiment')

		self._language = self._get_from_dictionary('language')

	@property
	def text(self):
		if self._text is None:
			self.tokenize()
		return self._text

	@property
	def sentences(self):
		"""
		:rtype: list[GoogleSentence]
		"""
		if self._sentences is None:
			self.tokenize()
		return self._sentences

	@property
	def tokens(self):
		"""
		:rtype: list[GoogleToken]
		"""
		if self._tokens is None:
			self.tokenize()
		return self._tokens

	@property
	def entities(self):
		"""
		:rtype: list[GoogleEntity]
		"""
		if self._entities is None:
			self.tokenize()
		return self._entities

	@property
	def sentiment(self):
		"""
		:rtype: GoogleSentiment
		"""
		if self._sentiment is None:
			self.tokenize()
		return self._sentiment

	@property
	def language(self):
		if self._language is None:
			self.tokenize()
		return self._language

	def graph_str(self):
		return '\n'.join([sentence.graph_str() for sentence in self.sentences])

	@property
	def graph(self):
		"""
		:rtype: Graph
		"""
		sentence_style = NodeStyle(text_size=7, shape='rect', style='"rounded, filled"')
		entity_style = NodeStyle(fill_colour='gold3', text_colour='black')
		mention_style = NodeStyle(fill_colour='gold', text_colour='black')

		if self._graph is None:
			self._graph = Graph()
			for token in self.tokens:
				self._graph.add_node(name=str(token.id), label=token.graph_str())

			if len(self._sentences) > 1:
				self._graph.add_node(
					name=str(self.id),
					label=f'{self.graph_str()}\n({len(self.sentences)} sentences)',
					style=sentence_style
				)

				for index, sentence in enumerate(self.sentences):
					self._graph.add_node(
						name=str(sentence.id),
						label=f'{sentence.graph_str()}\n(sentence {index+1})',
						style=sentence_style
					)
					self._graph.connect(start=str(self.id), end=str(sentence.id))  # document --> sentence
					for token in sentence.tokens:
						self._graph.connect(start=str(sentence.id), end=str(token.id))  # sentence --> token

			else:
				self._graph.add_node(
					name=str(self.id),
					label=f'{self.graph_str()}\n({len(self.sentences)} sentence)',
					style=sentence_style
				)
				for sentence in self.sentences:
					for token in sentence.tokens:
						self._graph.connect(start=str(self.id), end=str(token.id))  # document --> token

			for entity in self.entities:
				self._graph.add_node(
					name=str(entity.id),
					label=entity.graph_str(),
					style=entity_style
				)

				for index, mention in enumerate(entity.mentions):
					self._graph.add_node(
						name=str(mention.id),
						label=f'mention {index+1}',
						style=mention_style
					)
					self._graph.connect(start=str(mention.id), end=str(entity.id))  # entity <-- mention
					for token in mention.tokens:
						self._graph.connect(start=str(token.id), end=str(mention.id))  # mention <-- token

		return self._graph

