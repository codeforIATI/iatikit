# pyandi

A [query language](https://erikbern.com/2018/08/30/i-dont-want-to-learn-your-garbage-query-language.html) wrapper around [XPath](https://en.wikipedia.org/wiki/XPath), with some [IATI](https://iatistandard.org/)-related helpers included.

The name is an homage to its predecessor, [pyIATI](https://github.com/IATI/pyIATI).

## Installation

```shell
pip install -r requirements.txt
```

## Getting started

```python
import pyandi

pyandi.download_data()  # download all XML in the registry
pyandi.download_codelists()  # download all the codelists
pyandi.download_schemas()  # download all schemas
```

## Examples

[Take a look here.](examples.ipynb)

## TODO

Lots. At the moment this is for internal use; I’m just adding features as I need them.
