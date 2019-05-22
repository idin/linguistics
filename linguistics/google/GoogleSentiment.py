class GoogleSentiment:
	def __init__(self, score, magnitude):
		self._score = score
		self._magnitude = magnitude

	@property
	def score(self):
		return self._score

	@property
	def magnitude(self):
		return self._magnitude
