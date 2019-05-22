from repustate import Client


class RepustateClient:
	def __init__(self, api_key, cache=None):
		"""
		:param str api_key:
		:param disk.Cache.Cache cache:
		"""
		self._client = Client(api_key=api_key)

		self._cache = cache
		if self._cache:
			self.get_entities = self._cache.make_cached(
				id='repustate_get_entities_function',
				function=self._get_entities,
				sub_directory='get_entities'
			)
			self.get_sentiment = self._cache.make_cached(
				id='repustate_get_sentiment_function',
				function=self._get_sentiment,
				sub_directory='get_sentiment'
			)
		else:
			self.get_entities = self._get_entities
			self.get_sentiment = self._get_sentiment

	@property
	def client(self):
		"""
		:rtype: Client
		"""
		return self._client

	def _get_entities(self, text, lang='en'):
		if isinstance(text, str):
			return self.client.entities(text=text, lang=lang)
		else:
			raise TypeError(f'text should be a string but it is a {type(text)}!')

	def _get_sentiment(self, text, lang='en'):
		if isinstance(text, str):
			return self.client.sentiment(text=text, lang=lang)
		elif isinstance(text, list):
			return self.client.bulk_sentiment(items=text, lang=lang)

	@property
	def usage(self):
		return self.client.usage()

