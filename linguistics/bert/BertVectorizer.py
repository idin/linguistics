from .BertVectorizerModel import BertVectorizerModel
import torch


class BertVectorizer:
	def __init__(self, num_tokens=50):
		self._has_gpu = torch.cuda.device_count() > 0
		self._model = BertVectorizerModel(num_tokens=num_tokens)

		if self._has_gpu:
			self._device = torch.device('cuda')
			self._num_devices = torch.cuda.device_count()
			self._model.to(self._device)

		else:
			self._device = torch.device('cpu')
			self._num_devices = torch.get_num_threads()

		self._model.eval()

	def __repr__(self):
		device = ('GPU' if self._has_gpu else 'CPU')
		return f'<{self.__class__.__name__}_{device}x{self._num_devices}>'

	def __str__(self):
		return repr(self)

	def vectorize(self, text, device=None, get_num_tokens=False):
		"""
		:type text: str or list[str] or Series
		:type device: str or NoneType
		:rtype: numpy.array
		"""
		return self._model.vectorize(text=text, device=device or self._device, get_num_tokens=get_num_tokens)
