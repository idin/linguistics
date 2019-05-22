from slytherin import trim


class GoogleDocumentObject:
	def __init__(self, dictionary, document, begin, end):
		"""
		:param dict dictionary: any object from a document
		:type document: .GoogleDocument.GoogleDocument
		"""
		self._dictionary = dictionary
		self._document = document
		self._begin = begin
		self._end = end

	@property
	def begin(self):
		return self._begin

	@property
	def end(self):
		return self._end

	def __lt__(self, other):
		"""
		:type other: GoogleToken
		:rtype: bool
		"""
		if self.begin < other.begin and self.end < other.end:
			return True
		elif self.begin >= other.begin and self.end >= other.end:
			return False
		else:
			raise ValueError(f'Token "{self}" and "{other}" overlap!')

	def __gt__(self, other):
		return other.__lt__(self)

	def __le__(self, other):
		return not self.__gt__(other)

	def __ge__(self, other):
		return not self.__lt__(other)

	@property
	def document(self):
		"""
		:rtype: .GoogleDocument.GoogleDocument
		"""
		return self._document

	def __str__(self):
		return self._dictionary.__str__()

	def graph_str(self):
		return trim(string=str(self), max_length=50, cut_from='middle')

	@property
	def id(self):
		return None

	def __eq__(self, other):
		return self.id == other.id

	def __ne__(self, other):
		return self.id != other.id

	@property
	def cloud(self):
		"""
		:rtype: .GoogleCloud.GoogleCloud
		"""
		return self.document.cloud
