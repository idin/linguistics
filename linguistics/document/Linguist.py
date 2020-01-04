import warnings
import spacy
from spacy.lang.en import English
from .Document import Document


class Linguist:
	def __init__(self, spacy_core='en_core_web_sm', prefer_gpu=None, wikipedia_api=None):
		if prefer_gpu is None:
			self._gpu = spacy.prefer_gpu()
		elif prefer_gpu:  # explicit True
			self._gpu = spacy.prefer_gpu()
			if not self._gpu:
				warnings.warn('GPU is not working!')
		else:
			self._gpu = False

		self._nlp = spacy.load(spacy_core)
		self._wikipedia = wikipedia_api

	@property
	def nlp(self):
		"""
		:rtype: English
		"""
		return self._nlp

	def create_document(self, text):
		doc = self.nlp(text)
		return Document(_doc=doc, nlp=self.nlp)

	def analyze(self, text):
		return self.create_document(text=text)


