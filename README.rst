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

.. image:: https://img.shields.io/travis/pwyf/iatikit/master.svg
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/pwyf/iatikit

.. image:: https://img.shields.io/coveralls/github/pwyf/iatikit/master.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/pwyf/iatikit?branch=master

iatikit is a toolkit for using `IATI data <https://iatistandard.org/>`__.
It includes a query language wrapper around
`XPath <https://en.wikipedia.org/wiki/XPath>`__, to make dealing with disparate
IATI versions easier.

The name was inspired by `Open Contracting <https://www.open-contracting.org/>`__’s
`ocdskit <https://pypi.org/project/ocdskit/>`__.

Installation
------------

iatikit is tested for pythons 2.7, 3.4, 3.5, 3.6 and 3.7.

You can install it using ``pip``:

.. code:: shell

    pip install iatikit

Documentation
-------------

Check out `Read the Docs <https://iatikit.readthedocs.io>`__!

Roadmap
-------

The `github issue
tracker <https://github.com/pwyf/iatikit/issues>`__ will hopefully provide
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

iatikit is `deployed to pypi <https://pypi.org/project/iatikit/>`__ automatically `by Travis <https://travis-ci.org/pwyf/iatikit>`__, whenever a new `tag is pushed to github <https://github.com/pwyf/iatikit/tags>`__.

License
-------

This work is `MIT licensed <https://github.com/pwyf/iatikit/blob/master/LICENSE.md>`__.
