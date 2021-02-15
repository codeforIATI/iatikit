iatikit
=======

.. image:: https://img.shields.io/pypi/v/iatikit.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/iatikit/

.. image:: https://img.shields.io/pypi/l/iatikit.svg
    :alt: License
    :target: https://pypi.org/project/iatikit/

.. image:: https://img.shields.io/pypi/pyversions/iatikit.svg
    :alt: Supported versions
    :target: https://pypi.org/project/iatikit/

.. image:: https://github.com/codeforIATI/iati-datastore/workflows/CI/badge.svg?branch=main
    :alt: Build Status
    :target: https://github.com/codeforIATI/iati-datastore/actions?query=workflow%3ACI

.. image:: https://img.shields.io/coveralls/github/codeforIATI/iatikit/main.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/codeforIATI/iatikit?branch=main

iatikit is a toolkit for using `IATI data <https://iatistandard.org/>`__.
It includes a query language wrapper around
`XPath <https://en.wikipedia.org/wiki/XPath>`__, to make dealing with disparate
IATI versions easier.

The name was inspired by `Open Contracting <https://www.open-contracting.org/>`__’s
`ocdskit <https://pypi.org/project/ocdskit/>`__.

Installation
------------

iatikit is tested for pythons 3.5, 3.6, 3.7 and 3.8.

You can install it using ``pip``:

.. code:: shell

    pip install iatikit

Documentation
-------------

Check out `Read the Docs <https://iatikit.readthedocs.io>`__!

Roadmap
-------

The `github issue
tracker <https://github.com/codeforIATI/iatikit/issues>`__ will hopefully provide
some idea.

Development
-----------

You can set up a local version by creating a virtualenv and running:

.. code:: shell

    pip install -r requirements_dev.txt

You can run tests with:

.. code:: shell

    pytest

Deployment
----------

iatikit is `deployed to pypi <https://pypi.org/project/iatikit/>`__ automatically by GitHub Actions whenever a new `tag is pushed to github <https://github.com/codeforIATI/iatikit/tags>`__.

License
-------

This work is `MIT licensed <https://github.com/codeforIATI/iatikit/blob/main/LICENSE.md>`__.
