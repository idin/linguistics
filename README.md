# Linguistics
Linguistics is a Python library for natural language processing.

## Installation
You can use pip to install linguistics.
```bash
pip install linguistics
```

## Dependencies
Linguistics uses Abstract and Graphviz to visualize graphs of the document.

## Usage

### *Document*
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

### Masking
