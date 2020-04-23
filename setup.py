from setuptools import setup, find_packages
# manually make sure en_core_web_sm is installed
import os
try:
	import spacy
	spacy.prefer_gpu()
	
	try:
		nlp = spacy.load('en_core_web_sm')
	except:
		os.system('python -m spacy download en')
except:
	os.system('pip install spacy')
	os.system('python -m spacy download en')
	try:
		nlp = spacy.load('en_core_web_sm')
	except:
		os.system('python -m spacy download en')


def readme():
	with open('./README.md') as f:
		return f.read()


setup(
	name='linguistics',
	version='2020.4.6',
	license='MIT',
	url='https://github.com/idin/linguistics',
	author='Idin',
	author_email='py@idin.ca',
	description='Python library for natural language processing',
	long_description=readme(),
	long_description_content_type='text/markdown',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Software Development :: Libraries :: Python Modules'
	],
	packages=find_packages(exclude=["jupyter_tests", ".idea", ".git"]),
	install_requires=[
		'abstract', 'spacy', 'requests', 'jellyfish', 'editdistance', 'chronometry',
		'slytherin', 'numpy', 'pandas',
		'torch', 'transformers'
	],
	python_requires='~=3.6',
	zip_safe=False
)
