Getting started
===============

Installation
------------

iatikit is tested for pythons 2.7, 3.5 and 3.6.

You can install iatikit using ``pip``:

.. code:: shell

    pip install iatikit

If you’re on Windows, we recommend using `Jupyter Notebook <https://jupyter.org/>`__, which you can get by `installing Anaconda <https://www.anaconda.com/distribution/#download-section>`__.

Once installed, you can run the following inside a Jupyter Notebook to install iatikit:

.. code:: python

    import sys

    !{sys.executable} -m pip install iatikit

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
