from .NounChunk import NounChunk
from .Entity import Entity
from .BasicToken import BasicToken
from .EntityChunk import EntityChunk
from .EntityType import EntityType
from .Sentence import Sentence
from .remove_list_duplicates import remove_list_duplicates
from .join_punctuation import join_punctuation
from .split_into_sentences import split_into_sentences

from abstract import Graph
from abstract.graph_style import NodeStyle
import spacy


class Token(BasicToken):
	def __init__(self, obj, document):
		super().__init__(obj=obj, document=document)
		self._parents = None
		self._children = None

	def __add__(self, other):
		"""
		:param Token or Document other: adding two tokens (or several tokens) creates a Document
		:rtype: Document
		"""
		return Document(text=str(self).rstrip()+' '+str(other).lstrip(), nlp=self.nlp)

	@property
	def parents(self):
		"""
		:rtype: list[Token]
		"""
		if self._parents is None:
			self._parents = [Token(obj=x, document=self.document) for x in self.token.ancestors]
		return self._parents

	@property
	def children(self):
		"""
		:rtype: list[Token]
		"""
		if self._children is None:
			self._children = [Token(obj=x, document=self.document) for x in self.token.children]
		return self._children


class Document:
	def __init__(self, text=None, nlp=None, id=0, _doc=None):
		"""
		:type text: str
		"""
		spacy.prefer_gpu()
		if isinstance(text, list):
			text = ' '.join([str(x) for x in text])
		self._id = id

		if text is None and _doc is None:
			raise ValueError('Either text or _doc should be given!')
		elif text is None:
			self._doc = _doc
			self._text = _doc.text
			self._nlp = nlp
		elif _doc is None:
			self._doc = None
			self._text = str(text)
			self._nlp = nlp or spacy.load('en_core_web_sm')
		else:
			raise ValueError('Either text or _doc should be None!')

		self._doc = None
		self._tokens = None
		self._noun_chunks = None
		self._entity_chunks = None
		self._entities = None
		self._sentences = None
		self._sentences_method = None
		self._entity_graph = None
		self._syntax_graph = None

	@property
	def nlp(self):
		"""
		:rtype: spacy.tokens.doc.Doc or NoneType
		"""
		return self._nlp

	@property
	def text(self):
		return self._text

	def tokenize(self):
		self._tokens = remove_list_duplicates([Token(obj=x, document=self) for x in self.doc])
		self._entities = remove_list_duplicates([Entity(obj=span, document=self) for span in self.doc.ents])
		self._noun_chunks = remove_list_duplicates([
			NounChunk(obj=span, document=self) for span in self.doc.noun_chunks
		])
		self._entity_chunks = remove_list_duplicates([EntityChunk(entity=entity) for entity in self._entities])

	@property
	def id(self):
		return self._id

	@property
	def doc(self):
		"""
		:rtype: tokens.Doc
		"""
		if self._doc is None:
			self._doc = self._nlp(self._text)
		return self._doc

	def __repr__(self):
		return self.doc.__repr__()

	def __str__(self):
		return self.doc.__str__()

	def graph_str(self):
		if len(str(self)) > 50:
			return f'{self}'[0:47] + '...'
		else:
			return str(self)

	@property
	def sentences(self):

		"""
		uses spacy to split a Document class into a list of Sentence objects
		:rtype: list[Sentence]
		"""
		if self._sentences is None:
			self._sentences = self.get_sentences(method='spacy', return_type='Sentence')
		return self._sentences

	def get_sentences(self, method='spacy', return_type='Sentence'):

		"""
		:param str method: can be spacy, regex
		:param str return_type: if method is spacy, return_type can be str or Sentence
		:rtype: list[str] or list[Sentence]
		"""

		return_type = return_type.lower()

		sentence_method = method.lower()
		self._sentences_method = sentence_method

		if sentence_method == 'spacy':
			self._sentences = [Sentence(obj=x, document=self) for x in self.doc.sents]
			'''
			elif sentence_method == 'nltk':
				self._sentences = nltk.sent_tokenize(text=self.text)
			'''
		elif sentence_method == 'regex':
			self._sentences = split_into_sentences(text=self.text)

		else:
			raise ValueError(f'method:{method} is unknown!')

		if return_type == 'str':
			return [str(x) for x in self._sentences]

		elif return_type == 'document':
			return [Document(text=str(x)) for x in self._sentences]

		else:
			return self._sentences

	@property
	def tokens(self):

		"""
		:rtype: list[Token]
		"""
		if self._tokens is None:
			self.tokenize()
		return self._tokens

	@property
	def entities(self):
		"""
		:rtype: list[Entity]
		"""
		if self._entities is None:
			self.tokenize()
		return self._entities

	@property
	def noun_chunks(self):
		"""
		:rtype: list[NounChunk]
		"""
		if self._noun_chunks is None:
			self.tokenize()
		return self._noun_chunks

	@property
	def entity_chunks(self):
		"""
		:rtype: list[EntityChunk]
		"""
		if self._entity_chunks is None:
			self.tokenize()
		return self._entity_chunks

	@property
	def entity_graph(self):
		"""
		:rtype: Graph
		"""
		sentence_style = NodeStyle(text_size=7, shape='rect', shape_style='"rounded, filled"')
		noun_chunk_style = NodeStyle(
			fill_colour='lightpink', text_colour='black', text_size=8,
			shape='rect', shape_style='"rounded, filled"'
		)
		entity_style = NodeStyle(fill_colour='gold3', text_colour='black')
		entity_chunk_style = NodeStyle(fill_colour='gold', text_colour='black')

		if self._entity_graph is None:
			self._entity_graph = Graph(ordering=False)
			# add sentences to the graph
			if len(self.sentences) > 1:
				self._entity_graph.add_node(
					name=str(self.id), label=f'{self.graph_str()}\n({len(self.sentences)} sentences)',
					style=NodeStyle(text_size=7, shape='rect', shape_style='"rounded, filled"')
				)
				for i, sentence in enumerate(self.sentences):
					self._entity_graph.add_node(
						name=str(sentence.id), label=f'{sentence.graph_str()}\n(sentence {i+1})',
						style=sentence_style
					)
					self._entity_graph.connect(start=str(self.id), end=str(sentence.id))
			else:
				for sentence in self.sentences:
					self._entity_graph.add_node(
						name=str(sentence.id), label=f'{sentence.graph_str()}\n(one sentence)',
						style=sentence_style
					)

			# add tokens to the graph
			for token in self.tokens:
				self._entity_graph.add_node(
					name=str(token.id), label=f'{token.graph_str()}',
					style=NodeStyle(text_size=8, shape='rect', shape_style='"rounded, filled"')
				)

			# add noun_chunks to the graph
			for noun_chunk in self.noun_chunks:
				self._entity_graph.add_node(
					name=str(noun_chunk.id), label=f'{noun_chunk.graph_str()}',
					style=noun_chunk_style
				)

				# noun_chunk to its tokens
				for token in noun_chunk.tokens:
					self._entity_graph.connect(start=str(token.noun_chunk.id), end=str(token.id))

			# connect tokens to sentences (only the ones that don't have a noun chunk parent)
			for sentence in self.sentences:
				noun_chunks_connected_to_this_sentence = []
				for token in sentence.tokens:
					if not token.noun_chunk:
						self._entity_graph.connect(start=str(sentence.id), end=str(token.id))
					else:
						noun_chunk = token.noun_chunk
						if noun_chunk not in noun_chunks_connected_to_this_sentence:
							self._entity_graph.connect(start=str(sentence.id), end=str(noun_chunk.id))
							noun_chunks_connected_to_this_sentence.append(noun_chunk)

			# add entities to the graph
			for entity in self.entities:
				self._entity_graph.add_node(
					name=str(entity.id), label=f'{entity.graph_str()}',
					style=entity_style
				)
				# connect entity to its tokens
				for token in entity.tokens:
					self._entity_graph.connect(start=str(token.id), end=str(entity.id))

			# add entity_chunks to the graph
			for entity_chunk in self.entity_chunks:
				self._entity_graph.add_node(
					name=str(entity_chunk.id), label=f'{entity_chunk.graph_str()}',
					style=entity_chunk_style
				)

				# connect entity_chunk to its entities
				for entity in entity_chunk.entities:
					self._entity_graph.connect(start=str(entity.id), end=str(entity_chunk.id))

		return self._entity_graph

	@property
	def syntax_graph(self):
		"""
		:rtype: Graph
		"""
		sentence_style = NodeStyle(text_size=7, shape='rect', shape_style='"rounded, filled"')
		if self._syntax_graph is None:
			self._syntax_graph = Graph(ordering=False)

			# add sentences to the graph
			for sentence in self.sentences:
				self._syntax_graph.add_node(
					name=str(sentence.id),
					label=f'{sentence.graph_str()}\n(sentence)',
					style=sentence_style
				)

			for token in self.tokens:
				self._syntax_graph.add_node(name=str(token.id), label=token.graph_str())

			# connect tokens to sentences
			for sentence in self.sentences:
				for token in sentence.tokens:
					# only connect root tokens (tokens without parents) to the sentence
					if len(token.parents) < 1:
						self._syntax_graph.connect(start=str(sentence.id), end=str(token.id))

			for token in self.tokens:
				for child in token.children:
					dependency_label = str(child.dependency).replace('_', '\n')
					self._syntax_graph.connect(start=str(token.id), end=str(child.id), label=dependency_label)
		return self._syntax_graph

	def __add__(self, other):
		"""
		:type other: Document or Token
		:rtype: Document
		"""
		return self.__class__(text=str(self).rstrip()+' '+str(other).lstrip())

	def bind(self, chunk_type='entity_chunk'):
		"""
		:param str chunk_type: can be one of entity_chunk, noun_chunk, or entity
		:rtype: list[Token or EntityChunk or NounChunk or Entity]
		"""
		if chunk_type == 'entity_chunk':
			chunks = [x for x in self.tokens if x.entity_chunk is None] + self.entity_chunks
		elif chunk_type == 'entity':
			chunks = [x for x in self.tokens if x.entity is None] + self.entities
		elif chunk_type == 'noun_chunk':
			chunks = [x for x in self.tokens if x.noun_chunk is None] + self.noun_chunks
		else:
			raise ValueError(f'chunk_type "{chunk_type}" is not acceptable!')
		return sorted(chunks, key=lambda x: x.start)

	def mask_entity_types(self, entity_types, chunk_type='entity_chunk'):
		"""
		:param list[str] or list[EntityType] or str entity_types: entity types to be masked, it can be 'all'
		:param str chunk_type: can be one of entity_chunk, noun_chunk, or entity
		:rtype: str
		"""
		if entity_types == 'all':
			pass
		else:
			entity_types = [EntityType(name=x) if not isinstance(x, EntityType) else x for x in entity_types]
		chunks = self.bind(chunk_type=chunk_type)
		strings = []
		for chunk in chunks:
			string = str(chunk)
			if (chunk_type == 'entity_chunk' and isinstance(chunk, EntityChunk)) or \
				(chunk_type == 'noun_chunk' and isinstance(chunk, NounChunk)):
				for entity_type in sorted(chunk.entity_types):
					if entity_types == 'all':
						string = f'<{entity_type.long_name.upper()}>'
						break
					elif entity_type in entity_types:
						string = f'<{entity_type.long_name.upper()}>'
						break
			elif chunk_type == 'entity' and isinstance(chunk, Entity):
				if entity_types == 'all':
					string = f'<{chunk.entity_type.long_name.upper()}>'
				elif chunk.entity_type in entity_types:
					string = f'<{chunk.entity_type.long_name.upper()}>'
			strings.append(string)
		return ' '.join(join_punctuation(seq=[str(x) for x in strings]))
