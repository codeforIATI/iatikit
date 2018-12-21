pyandi
======

A `query
language <https://erikbern.com/2018/08/30/i-dont-want-to-learn-your-garbage-query-language.html>`__
wrapper around `XPath <https://en.wikipedia.org/wiki/XPath>`__, with
some `IATI <https://iatistandard.org/>`__-related helpers included.

The name is an homage to its predecessor,
`pyIATI <https://github.com/IATI/pyIATI>`__.

Installation
------------

.. code:: shell

    pip install pyandi

Getting started
---------------

.. code:: python

    import pyandi

    # download all XML in the registry
    pyandi.download.data()

    # download all the codelists
    pyandi.download.codelists()

Examples
--------

Count datasets and publishers on the registry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()

    publishers = registry.publishers
    total_publishers = len(publishers)
    total_datasets = sum([len(pub.datasets) for pub in publishers])
    print('There are {:,} publishers and {:,} datasets on the registry'.format(
        total_publishers, total_datasets))

    # There are 855 publishers and 6,682 datasets on the registry

Count datasets for a publisher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()

    usaid = registry.publishers.find(name='usaid')
    print('USAID has {:,} datasets.'.format(len(usaid.datasets)))

    # USAID has 177 datasets.

Find an activity by its identifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()
    iati_identifier = 'GB-1-201724-151'

    dfid = registry.publishers.find(name='dfid')
    act = dfid.activities.where(
        iati_identifier=iati_identifier
    ).first()

    print(act)

    # <Activity (GB-1-201724-151)>

Find activities that include an element
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()

    mcc = registry.publishers.find(name='millenniumchallenge')
    total_with_locations = len(mcc.activities.where(location__exists=True))
    total_activities = len(mcc.activities)
    print('{:,} of {:,} MCC activities have location data.'.format(
        total_with_locations, total_activities))

    # 279 of 3,038 MCC activities have location data.

More complicated activity filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()

    dfid = registry.publishers.find(name='dfid')
    sector_category = pyandi.sector(311, 2)  # Agriculture

    ag_acts = dfid.activities.where(
        actual_start__lte='2017-12-31',
        actual_end__gte='2017-01-01',
        sector__in=sector_category,
    )
    print('DFID had {:,} agricultural activities running during 2017.'.format(
        len(ag_acts)))

    # DFID had 180 agricultural activities running during 2017.

TODO
----

Plenty! Refer to `the github issue
tracker <https://github.com/andylolz/pyandi/issues>`__.
