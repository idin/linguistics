import requests
from ..document.part_of_speach_definitions import PART_OF_SPEACH

_analyze_to_engine = {
	'entities': 'analyzeEntities',
	'entity_sentiment': 'analyzeEntitySentiment',
	'sentiment': 'analyzeSentiment',
	'syntax': 'analyzeSyntax',
	'all': 'annotateText',
	'document': 'classifyText'
}


def standardize_text(text):
	if 'beginOffset' in text:
		text['begin_offset'] = text.pop('beginOffset')


def standardize_token(token):
	if 'text' in token:
		text = token['text']
		standardize_text(text=text)

	if 'partOfSpeech' in token:
		part_of_speech = token.pop('partOfSpeech')
		token['part_of_speech'] = {
			key: standardirze_part_of_speech(value.lower()) if key == 'tag' else value.lower()
			for key, value in part_of_speech.items()
			if not value.endswith('_UNKNOWN')
		}

	if 'dependencyEdge' in token:
		dependency_edge = token.pop('dependencyEdge')
		if 'headTokenIndex' in dependency_edge:
			dependency_edge['head_token_index'] = dependency_edge.pop('headTokenIndex')
		if 'label' in dependency_edge:
			dependency_edge['label'] = dependency_edge['label'].lower()


def standardize_entity(entity):
	if 'type' in entity:
		entity['type'] = entity['type'].lower()
	if 'mentions' in entity:
		mentions = entity['mentions']
		for mention in mentions:
			if 'type' in mention:
				mention['type'] = mention['type'].lower()
			if 'text' in mention:
				text = mention['text']
				standardize_text(text=text)


def standardirze_part_of_speech(part_of_speech):
	if part_of_speech in PART_OF_SPEACH:
		return PART_OF_SPEACH[part_of_speech]
	else:
		return part_of_speech


def analyze(
		text, api_key, standardize=True, language='en',
		extract_entities=True, extract_sentiment=True, extract_syntax=True
):
	document = {
		"document": {
			"type": "PLAIN_TEXT",
			"language": language,
			"content": text
		},
		'features': {
			"extractEntities": extract_entities,
			"extractDocumentSentiment": extract_sentiment,
			"extractEntitySentiment": extract_entities and extract_sentiment,
			"extractSyntax": extract_syntax
		},
		"encodingType": "UTF8"
	}
	response = requests.post(
		f"https://language.googleapis.com/v1beta2/documents:annotateText?key={api_key}",
		json=document, verify=False
	)
	result = response.json()
	if standardize:
		if 'sentences' in result:
			sentences = result['sentences']
			for sentence in sentences:
				if 'text' in sentence:
					text = sentence['text']
					standardize_text(text=text)
		if 'tokens' in result:
			tokens = result['tokens']
			for token in tokens:
				standardize_token(token=token)
		if 'documentSentiment' in result:
			result['document_sentiment'] = result.pop('documentSentiment')
		if 'entities' in result:
			for entity in result['entities']:
				standardize_entity(entity=entity)
	result['text'] = text
	return result

