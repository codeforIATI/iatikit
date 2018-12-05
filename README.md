# pyandi

A [query language](https://erikbern.com/2018/08/30/i-dont-want-to-learn-your-garbage-query-language.html) wrapper around [XPath](https://en.wikipedia.org/wiki/XPath), with some [IATI](https://iatistandard.org/)-related helpers included.

The name is an homage to its predecessor, [pyIATI](https://github.com/IATI/pyIATI).

## Installation

```shell
pip install pyandi
```

## Getting started

```python
import pyandi

# download all XML in the registry
pyandi.download.data()

# download all the codelists
pyandi.download.codelists()

# download all schemas
pyandi.download.schemas()
```

## Examples

### Count datasets and publishers on the registry

```python
import pyandi

publishers = pyandi.publishers()
total_publishers = len(publishers)
total_datasets = sum([len(pub.datasets) for pub in publishers])
print('There are {:,} publishers and {:,} datasets on the registry'.format(
    total_publishers, total_datasets))

# There are 855 publishers and 6,682 datasets on the registry
```

### Count datasets for a publisher

```python
import pyandi

usaid = pyandi.publishers().find(name='usaid')
print('USAID have {:,} datasets.'.format(len(usaid.datasets)))

# USAID have 177 datasets.
```

### Find an activity by its identifier

```python
import pyandi

iati_identifier = 'GB-1-201724-151'

dfid = pyandi.publishers().find(name='dfid')
act = dfid.activities.where(
    iati_identifier=iati_identifier
).first()

print(act)

# Developing methods for measuring the deforestation avoided as a result of International Climate Fund projects (GB-1-201724-151)
```

### Find activities that include an element

```python
import pyandi

mcc = pyandi.publishers().find(name='millenniumchallenge')
total_with_locations = len(mcc.activities.where(location__exists=True))
total_activities = len(mcc.activities)
print('{:,} of {:,} MCC activities have location data.'.format(
    total_with_locations, total_activities))

# 279 of 3,038 MCC activities have location data.
```

### More complicated activity filters

```python
import pyandi

dfid = pyandi.publishers().find(name='dfid')

ag_acts = dfid.activities.where(
    actual_start__lte='2017-12-31',
    actual_end__gte='2017-01-01',
    sector__startswith='311',  # Agriculture
)
print('DFID had {:,} agricultural activities running during 2017.'.format(
    len(ag_acts)))

# DFID had 176 agricultural activities running during 2017.
```

## TODO

Lots. At the moment this is for internal use; I’m just adding features as I need them.
