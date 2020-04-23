import torch
import torch.nn as nn
from torch import Tensor
from pandas import Series
from transformers import BertTokenizer
from transformers import BertModel


class BertVectorizerModel(nn.Module):
	def __init__(self, num_tokens=50):
		super().__init__()
		self._bert_layer = BertModel.from_pretrained('bert-base-uncased')
		self._tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
		self._num_tokens = num_tokens

		self._classification_layer = nn.Linear(768, 1)
		self._activation_layer = nn.Sigmoid()

	def forward(self, sequence, attention_mask):
		"""

		:param sequence: Tensor of shape [B, T] containing token ids of sequences
		:param attention_mask: Tensor of shape [B, T] containing attention masks to be used to avoid contribution of PAD tokens
		:return:
		"""

		#  feed the input to BERT to obtain contextualized representations
		contextualized_representations, _ = self._bert_layer(sequence, attention_mask=attention_mask)

		#  obtain the representation of [CLS] head
		classification_representation = contextualized_representations[:, 0]

		return classification_representation

	def clean_text(self, string, get_num_tokens=False):
		"""
		:type string: str
		:rtype: Tensor
		"""
		tokens = ['[CLS]'] + self._tokenizer.tokenize(string) + ['[SEP]']
		num_tokens = len(tokens)

		if len(tokens) > self._num_tokens:
			tokens = tokens[: self._num_tokens - 1] + ['[SEP]']
		else:
			tokens += ['[PAD]'] * (self._num_tokens - len(tokens))

		token_ids = self._tokenizer.convert_tokens_to_ids(tokens)
		# token_ids_tensor = torch.tensor(token_ids)

		result = token_ids
		if get_num_tokens:
			return result, num_tokens
		else:
			return result

	def vectorize(self, text, device=None, get_num_tokens=False):
		"""
		:type text: str or list[str] or Series
		:type device: str or NoneType
		:type get_num_tokens: bool
		:rtype: numpy.array
		"""
		if len(text) == 0:
			if get_num_tokens:
				return None, None
			else:
				return None

		if isinstance(text, (list, Series)):
			_cleaned_text = [self.clean_text(sentence, get_num_tokens=get_num_tokens) for sentence in text]
		elif isinstance(text, str):
			_cleaned_text = [self.clean_text(text, get_num_tokens=get_num_tokens)]
		else:
			raise TypeError(f'text cannot be of type {type(text)}')

		if get_num_tokens:
			cleaned_text = [x[0] for x in _cleaned_text]
			num_tokens = [x[1] for x in _cleaned_text]
		else:
			cleaned_text = _cleaned_text
			num_tokens = None

		sequence = torch.tensor(cleaned_text)
		if device:
			sequence = sequence.to(device)

		attention_mask = torch.stack(
			[(sentence != 0).long() for sentence in sequence]
		)

		if device:
			attention_mask = attention_mask.to(device)

		result = self.forward(sequence=sequence, attention_mask=attention_mask).cpu().data.numpy()
		if get_num_tokens:
			return result, num_tokens
		else:
			return result
















