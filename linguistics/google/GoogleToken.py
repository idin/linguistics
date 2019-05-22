from .GoogleDocumentObject import GoogleDocumentObject


class GoogleToken(GoogleDocumentObject):
	def __init__(self, dictionary, document):
		text = dictionary.pop('text')
		content = text.pop('content')
		begin = text.pop('begin_offset')
		end = begin + len(content)
		super().__init__(dictionary=dictionary, document=document, begin=begin, end=end)

		self._text = content
		self._grammer = self._dictionary.pop('part_of_speech')
		self._part_of_speech = self._grammer.pop('tag', None)
		self._number = self._grammer.pop('number', None)
		self._person = self._grammer.pop('person', None)
		self._index = None

	@property
	def id(self):
		return self.document.id, 'token', self._index

	@property
	def index(self):
		return self._index

	@property
	def begin(self):
		return self._begin

	@property
	def end(self):
		return self._end

	@property
	def text(self):
		return self._text

	@property
	def part_of_speech(self):
		return self._part_of_speech

	@property
	def number(self):
		return self._number

	@property
	def person(self):
		return self._person

	def __repr__(self):
		return str(self._text)

	def __str__(self):
		return f'{self.text}'

	def graph_str(self):
		if self.part_of_speech:
			part_of_speech = f"\n{self.part_of_speech.replace('_', ' ')}"
		else:
			part_of_speech = ''
		return f"[{self.index}] '{self}'" + part_of_speech


	def __eq__(self, other):
		return self._text == other._text and self._begin == other._begin and self._end == other._end
