Getting started
===============

Installation
------------

iatikit is tested for pythons 3.7 – 3.9.

You can install iatikit using ``pip``:

.. code:: shell

    pip install iatikit

If you’re on Windows, we recommend using `Jupyter Notebook <https://jupyter.org/>`__, which you can get by `installing Anaconda <https://www.anaconda.com/distribution/#download-section>`__.

Once Jupyter is installed, you can run the following inside a Notebook to install iatikit:

.. code:: python

    import sys

    !{sys.executable} -m pip install --upgrade iatikit

Setup
-----

Once iatikit is installed, you’ll need to fetch a recent version of all IATI data
from `the registry <https://iatiregistry.org/>`__, as well as `the latest codelists <http://reference.iatistandard.org/codelists/>`__ and `schemas <http://reference.iatistandard.org/schema/>`__.

.. code:: python

    import iatikit

    # download all schemas and codelists
    iatikit.download.standard()

    # download all XML in the registry
    iatikit.download.data()

By default iatikit will download all the IATI data from the Code for IATI Data Download tool. However, you can customise this by creating an `iatikit.ini` file and using the following setting:

.. code:: ini

    [data_sources]
    zip_url=URL_OF_ZIP_FILE

The `iatikit.ini` file should be placed in the directory from which python is launched to run the client application (i.e., the application which uses `iatikit`). 
