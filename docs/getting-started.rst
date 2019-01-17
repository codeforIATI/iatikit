Getting started
===============

Installation
------------

iatikit is tested for pythons 2.7, 3.5 and 3.6.

You can install it using ``pip``:

.. code:: shell

    pip install iatikit

Setup
-----

Once installed, you’ll need to fetch a recent version of all IATI data
from `the registry <https://iatiregistry.org/>`__, as well as `the latest codelists <http://reference.iatistandard.org/codelists/>`__.

.. code:: python

    import iatikit

    # download all XML in the registry
    iatikit.download.data()

    # download all the codelists
    iatikit.download.codelists()
