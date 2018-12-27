Getting started
===============

Installation
------------

You can install pyandi using ``pip``:

.. code:: shell

    pip install pyandi

Setup
-----

Once installed, you’ll need to fetch a recent version of all IATI data
from `the registry <https://iatiregistry.org/>`__, as well as `the latest codelists <http://reference.iatistandard.org/codelists/>`__.

.. code:: python

    import pyandi

    # download all XML in the registry
    pyandi.download.data()

    # download all the codelists
    pyandi.download.codelists()
