Usage examples
==============

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

List all publishers by date of first publication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from datetime import datetime
    import pyandi

    registry = pyandi.data()

    publishers = sorted(
        [(min([d.metadata.get('metadata_created')
               for d in p.datasets]
              ), p.metadata.get('title'))
         for p in registry.publishers])

    for idx, tup in enumerate(publishers):
        print('{order}: {name} ({date})'.format(
            order=(idx + 1),
            name=tup[1],
            date=datetime.strptime(tup[0], '%Y-%m-%dT%H:%M:%S.%f').date()
        ))

    # 1: UK - Department for International Development (DFID) (2011-01-29)
    # 2: The William and Flora Hewlett Foundation (2011-03-31)
    # 3: The World Bank (2011-05-14)
    # ...

More complicated activity filters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import pyandi

    registry = pyandi.data()

    dfid = registry.publishers.find(name='dfid')
    sector_category = pyandi.sector(311, 2)  # Agriculture

    ag_acts = dfid.activities.where(
        actual_start__lte='2017-12-31',  # started before 2018
        actual_end__gte='2017-01-01',  # ended after 2016
        sector__in=sector_category,
    )
    print('DFID had {:,} agricultural activities running during 2017.'.format(
        len(ag_acts)))

    # DFID had 180 agricultural activities running during 2017.
