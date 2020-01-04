import requests


class Repustate:
	def __init__(self, api_key=None, server='api.repustate.com', cache=None):
		"""
		:param str api_key:
		:param disk.Cache.Cache cache:
		"""
		self._api_key = api_key or '$APIKEY'
		self._server = server

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
	def usage(self):
		response = requests.get(
			f'https://{self._server}/v4/{self._api_key}/usage.json',
			verify=False,
		)
		return response.json()

	def _get_entities(self, text, language='en'):
		response = requests.post(
			f'https://{self._server}/v4/{self._api_key}/entities.json',
			verify=False, data={'text': text, 'lang': language}
		)
		return response.json()

	def _get_sentiment(self, text, topics=None, language='en'):
		if isinstance(text, str):
			if topics is None:
				response = requests.post(
					f'https://{self._server}/v4/{self._api_key}/score.json',
					verify=False, data={'text': text, 'lang': language}
				)

			else:
				response = requests.post(
					f'https://{self._server}/v4/{self._api_key}/topic.json',
					verify=False, data={'text': text, 'topics': ','.join(topics) , 'lang': language}
				)

		elif isinstance(text, list):
			if topics is None:
				data = {f'text{i}': t for i, t in enumerate(text)}
				data['lang'] = language
				response = requests.post(
					f'https://{self._server}/v4/{self._api_key}/bulk-score.json',
					verify=False, data=data
				)
			else:
				response = None
		else:
			response = None

		return response.json()
