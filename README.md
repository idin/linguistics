# Linguistics
Linguistics is a Python library for natural language processing.

## Installation
You can use pip to install linguistics.
```bash
pip install linguistics
```

## Dependencies
Linguistics uses Abstract and Graphviz to visualize graphs of the document.

## Similarity

### Sentence

#### get_similar_pairs

```python
from linguistics.similarity import Sentence

sentence_1 = Sentence('John Joseph Nicholson')
sentence_2 = Sentence('Nicholson, Jack')
print(sentence_1.get_similar_pairs(sentence_2))
```
produces:
```json
[{'word_1': Nicholson,
  'word_2': Nicholson,
  'similarity': 1.0,
  'index_1': 2,
  'index_2': 0},
 {'word_1': John,
  'word_2': Jack,
  'similarity': 0.5,
  'index_1': 0,
  'index_2': 1},
 {'word_1': Joseph,
  'word_2': None,
  'similarity': 0,
  'index_1': 1,
  'index_2': None}]
```

#### get_unordered_similarity
```python
print(sentence_1.get_unordered_similarity(sentence_2))
print(sentence_1.get_unordered_similarity(sentence_2, case_sensitivity=0, weights=[1, 1]))
print(sentence_1.get_unordered_similarity(sentence_2, case_sensitivity=0, weights=[2, 1]))
print(sentence_1.get_unordered_similarity(sentence_2, case_sensitivity=0, weights=[1]))
print(sentence_1.get_unordered_similarity(sentence_2, case_sensitivity=0, first_char_weight=1, weights=[1, 1]))
```
produces
```json
0.5
0.75
0.8333333333333334
1.0
0.875
```


## *Document*
```python
from linguistics import Document

# create document
document = Document("He also begat and brought up five pairs of male children.")
```

### Entity Graph
```python
display(document.entity_graph.render())
```
![](https://github.com/idin/linguistics/blob/master/pictures/entity_graph.png?raw=true)

### Document Graph
```python
display(document.graph.render())
```
![](https://github.com/idin/linguistics/blob/master/pictures/document_graph.png?raw=true)
