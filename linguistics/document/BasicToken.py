from .DocumentObject import DocumentObject
from .dependency_definitions import DEPENDENCY_DEFINITONS
from .part_of_speach_definitions import PART_OF_SPEACH
from .EntityType import EntityType


class BasicToken(DocumentObject):
	def __init__(self, obj, document):
		"""
		:param obj: any object from a document
		:type document: Document
		"""
		super().__init__(obj=obj, document=document)
		self._entity = None
		self._noun_chunk = None
		self._entity_chunk = None
		if self._obj.ent_type_:
			self._entity_type = EntityType(name=self._obj.ent_type_)
		else:
			self._entity_type = None

	@property
	def index(self):
		"""
		:rtype: int
		"""
		return self.token.i

	@property
	def character_range(self):
		return self.token.idx, self.token.idx + len(self.token.text)

	@property
	def start(self):
		"""
		:rtype: int
		"""
		return self.index

	@property
	def end(self):
		"""
		:rtype: int
		"""
		return self.index

	def graph_str(self):
		return f"[{self.index}] '{self}'\n{self.part_of_speech.replace('_', ' ')}"

	@property
	def id(self):
		"""
		:rtype: tuple
		"""
		return (self.document.id, 'token', self.index)

	@property
	def token(self):
		"""
		:rtype: tokens.Token
		"""
		return self._obj

	@property
	def text(self):
		return self.token.text

	@property
	def lemma(self):
		return self.token.lemma_

	@property
	def part_of_speech(self):
		"""
		:rtype: str
		"""
		if self.token.pos_:
			lower = str(self.token.pos_).lower()
			if lower in PART_OF_SPEACH:
				return PART_OF_SPEACH[lower]
			else:
				return lower
		else:
			return self.token.pos_

	@property
	def tag(self):
		return self.token.tag_

	@property
	def dependency_code(self):
		"""
		:rtype: str
		"""
		return self.token.dep_

	@property
	def dependency(self):
		"""
		:rtype: str
		"""
		if self.dependency_code:
			lower = str(self.dependency_code).lower()
			if lower in DEPENDENCY_DEFINITONS:
				return DEPENDENCY_DEFINITONS[lower]
			else:
				return lower
		else:
			return self.dependency_code

	@property
	def shape(self):
		return self.token.shape_

	@property
	def is_alpha(self):
		return self.token.is_alpha

	@property
	def is_stop(self):
		return self.token.is_stop

	@property
	def is_punctuation(self):
		return self.part_of_speech == 'punctuation'

	@property
	def entity_iob(self):
		return self._obj.ent_iob_

	@property
	def entity_type(self):
		return self._entity_type

	@property
	def entity(self):
		"""
		:rtype: Entity
		"""
		return self._entity

	@property
	def noun_chunk(self):
		"""
		:rtype: NounChunk
		"""
		return self._noun_chunk

	@property
	def entity_chunk(self):
		"""
		:rtype: EntityChunk
		"""
		return self._entity_chunk
