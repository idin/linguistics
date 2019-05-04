from .TokenSpan import TokenSpan


class Sentence(TokenSpan):
	def __init__(self, obj, document):
		super().__init__(obj=obj, document=document)

	@property
	def id(self):
		return self.document.id, 'sentence', self.start, self.end
