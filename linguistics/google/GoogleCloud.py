from .analyze import analyze
from .GoogleDocument import GoogleDocument


class GoogleCloud:
	def __init__(
			self,
			api_key,
			language='english',
			standardize=True,
			extract_entities=True,
			extract_sentiment=True,
			extract_syntax=True,
			cache=None
	):
		"""
		:param str api_key:
		:param str language:
		:param bool standardize:
		:param bool extract_entities:
		:param bool extract_sentiment:
		:param bool extract_syntax:
		:param disk.Cache.Cache cache:
		"""
		self._api_key = api_key
		self._language = language[:2].lower()
		self._standardize = standardize
		self._extract_entities = extract_entities
		self._extract_sentiment = extract_sentiment
		self._extract_syntax = extract_syntax
		self._cache = cache
		if self._cache:
			self._cached_analyze = self._cache.make_cached(
				function=self._analyze, id='google_cloud_analyze_function',
				sub_directory='analyze'
			)
		else:
			self._cached_analyze = self._analyze

	def _analyze(
			self, text, language, standardize, extract_entities,
			extract_sentiment, extract_syntax
	):
		return analyze(
			text=text, api_key=self._api_key, language=language, standardize=standardize,
			extract_entities=extract_entities, extract_sentiment=extract_sentiment,
			extract_syntax=extract_syntax
		)

	def analyze(self, text):
		return self._cached_analyze(
			text=text,
			language=self._language,
			standardize=self._standardize,
			extract_entities=self._extract_entities,
			extract_sentiment=self._extract_sentiment,
			extract_syntax=self._extract_syntax
		)

	def create_document(self, text):
		analysis = self.analyze(text=text)
		return GoogleDocument(cloud=self, _analysis=analysis)

