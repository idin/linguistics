



class DocumentObject:
	def __init__(self, obj, document):
		"""
		:param obj: any object from a document
		:type document: Document
		"""
		self._obj = obj
		self._document = document

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
		return str(self)

	@property
	def id(self):
		return None

	def __eq__(self, other):
		return self.id==other.id

	def __ne__(self, other):
		return self.id!=other.id


