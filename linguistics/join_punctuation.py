

def join_punctuation(seq, characters='.,;?!'):
	characters = set(characters)
	seq = iter(seq)
	current = next(seq)

	for nxt in seq:
		if nxt in characters:
			current += nxt
		else:
			yield current
			current = nxt

	yield current

