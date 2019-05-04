from .analyze import analyze
from .Document import Document


class Cloud:
	def __init__(
			self,
			api_key,
			language='english',
			standardize=True,
			extract_entities=True,
			extract_sentiment=True,
			extract_syntax=True
	):
		self._api_key = api_key
		self._language = language[:2].lower()
		self._standardize = standardize
		self._extract_entities = extract_entities
		self._extract_sentiment = extract_sentiment
		self._extract_syntax = extract_syntax

	def analyze(self, text):
		return analyze(
			text=text,
			api_key=self._api_key,
			language=self._language,
			standardize=self._standardize,
			extract_entities=self._extract_entities,
			extract_sentiment=self._extract_sentiment,
			extract_syntax=self._extract_syntax
		)

	def create_document(self, text):
		analysis = self.analyze(text=text)
		return Document(cloud=self, _analysis=analysis)

