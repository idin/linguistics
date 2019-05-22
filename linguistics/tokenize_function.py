import re

WORD = re.compile(r'\w+')


def tokenize(text):
	"""
	this function tokenizes text at a very high speed
	:param str text: text to be tokenized
	:rtype: list[str]
	"""
	words = WORD.findall(text)
	return words
