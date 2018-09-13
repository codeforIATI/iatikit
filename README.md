# pyandi

A [query language](https://erikbern.com/2018/08/30/i-dont-want-to-learn-your-garbage-query-language.html) wrapper around [XPath](https://en.wikipedia.org/wiki/XPath), with some [IATI](https://iatistandard.org/)-related helpers included.

The name is a homage to its predecessor, [pyIATI](https://github.com/IATI/pyIATI).

## Installation

```shell
pip install -r requirements.txt
```

## Getting started

```python
import pyandi

pyandi.refresh_data()  # download all XML in the registry
pyandi.refresh_codelists()  # download all the codelists
```

## Examples

```python
usaid = pyandi.PublisherSet(path='pyandi/data').find(name='usaid')
print('USAID have {} datasets.'.format(len(usaid.datasets)))
# USAID have 177 datasets.

ag_acts = usaid.activities.where(
    actual_start__lte='2017-12-31',
    actual_end__gte='2017-01-01',
    transaction_sector__startswith='311',  # Agriculture
)
print('USAID had {} agricultural activities running during 2017.'.format(
    len(ag_acts)))
# USAID had 1461 agricultural activities running during 2017.
```
