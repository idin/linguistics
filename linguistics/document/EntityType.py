from collections import OrderedDict

# source: https://spacy.io/usage/linguistic-features
ENTITY_TYPES_BY_SHORTNAME = OrderedDict([
	('PERSON', ('People, including fictional', 'person')),
	('NORP', ('Nationalities or religious or political groups', 'group')),
	('FAC', ('Buildings, airports, highways, bridges, etc', 'facility')),
	('ORG', ('Companies, agencies, institutions, etc', 'organization')),
	('GPE', ('Countries, cities, states', 'geopolitical_entity')),
	('LOC', ('Non-GPE locations, mountain ranges, bodies of water', 'location')),
	('PRODUCT', ('Objects, vehicles, foods, etc (Not services)', 'product')),
	('EVENT', ('Named hurricanes, battles, wars, sports events, etc', 'event')),
	('WORK_OF_ART', ('Titles of books, songs, etc', 'word_of_art')),
	('LAW', ('Named documents made into laws', 'law')),
	('LANGUAGE', ('Any named language', 'language')),
	('DATE', ('Absolute or relative dates or periods', 'date')),
	('TIME', ('Times smaller than a day', 'time')),
	('PERCENT', ('Percentage, including "%"', 'percent')),
	('MONEY', ('Monetary values, including unit', 'money')),
	('QUANTITY', ('Measurements, as of weight or distance', 'quantity')),
	('ORDINAL', ('"first", "second", etc', 'ordinal')),
	('CARDINAL', ('Numerals that do not fall under another type', 'cardinal'))
])

ENTITY_TYPES_BY_LONGNAME = OrderedDict()
for shortname, definition_longname in ENTITY_TYPES_BY_SHORTNAME.items():
	definition, longname = definition_longname
	ENTITY_TYPES_BY_LONGNAME[longname] = (definition, shortname)


class EntityType:
	def __init__(self, name):
		name_upper = str(name).upper()
		name_lower = str(name).lower()
		self._short_name = name_upper
		self._long_name = name_lower
		self._description = name
		if name_upper in ENTITY_TYPES_BY_SHORTNAME:
			entity_description_and_long_name = ENTITY_TYPES_BY_SHORTNAME[name_upper]
			self._description = entity_description_and_long_name[0]
			self._long_name = entity_description_and_long_name[1].lower()
			self._index = list(ENTITY_TYPES_BY_SHORTNAME.keys()).index(name_upper)
		elif name_lower in ENTITY_TYPES_BY_LONGNAME:
			entity_description_and_long_name = ENTITY_TYPES_BY_LONGNAME[name_lower]
			self._description = entity_description_and_long_name[0]
			self._short_name = entity_description_and_long_name[1]
			self._index = list(ENTITY_TYPES_BY_LONGNAME.keys()).index(name_lower)

	@property
	def short_name(self):
		return self._short_name

	@property
	def description(self):
		return self._description

	@property
	def long_name(self):
		return self._long_name

	@property
	def index(self):
		return self._index

	@property
	def id(self):
		return (self.index, self.short_name)

	def __str__(self):
		return self.long_name

	def __repr__(self):
		return self.long_name

	def __lt__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id < other.id

	def __eq__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id == other.id

	def __gt__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id > other.id

	def __le__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id <= other.id

	def __ge__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id >= other.id

	def __ne__(self, other):
		"""
		:type other: EntityType
		:rtype: bool
		"""
		return self.id != other.id



