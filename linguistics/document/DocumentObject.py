from slytherin import trim

class DocumentObject:
	def __init__(self, obj, document):
		"""
		:param obj: any object from a document
		:type document: Document
		"""
		self._obj = obj
		self._document = document

	@property
	def nlp(self):
		return self.document.nlp

	@property
	def document(self):
		"""
		:rtype: Document
		"""
		return self._document

	def __repr__(self):
		return self._obj.__repr__()

	def __str__(self):
		return self._obj.__str__()

	def graph_str(self):
		return trim(string=str(self), max_length=50, cut_from='middle')

	@property
	def id(self):
		return None

	def __eq__(self, other):
		return self.id == other.id

	def __ne__(self, other):
		return self.id != other.id
