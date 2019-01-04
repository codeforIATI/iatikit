pyandi
======

.. image:: https://img.shields.io/pypi/v/pyandi.svg
    :target: https://pypi.org/project/pyandi/

.. image:: https://img.shields.io/pypi/l/pyandi.svg
    :target: https://pypi.org/project/pyandi/

.. image:: https://img.shields.io/pypi/pyversions/pyandi.svg
    :target: https://pypi.org/project/pyandi/

.. image:: https://img.shields.io/travis/pwyf/pyandi/master.svg
    :target: https://travis-ci.org/pwyf/pyandi

.. image:: https://img.shields.io/coveralls/github/pwyf/pyandi/master.svg
    :target: https://coveralls.io/github/pwyf/pyandi?branch=master

pyandi is a toolkit for using `IATI data <https://iatistandard.org/>`__. It includes a `query
language <https://erikbern.com/2018/08/30/i-dont-want-to-learn-your-garbage-query-language.html>`__
wrapper around `XPath <https://en.wikipedia.org/wiki/XPath>`__,
to make dealing with disparate IATI versions easier.

The name is a homage to its predecessor,
`pyIATI <https://github.com/IATI/pyIATI>`__.

Installation
------------

pyandi is tested for python 2.7, 3.5 and 3.6.

You can install it using ``pip``:

.. code:: shell

    pip install pyandi

Documentation
-------------

Check out `Read the Docs <https://pyandi.readthedocs.io>`__!

Roadmap
-------

The `github issue
tracker <https://github.com/pwyf/pyandi/issues>`__ will hopefully provide
some idea.

Development
-----------

You can set up a local version by creating a virtualenv and running:

.. code:: shell

    pip install -r requirements_dev.txt

You can run tests with:

.. code:: shell

    tox

Deployment
----------

pyandi is `deployed to pypi <https://pypi.org/project/pyandi/>`__ automatically `by Travis <https://travis-ci.org/pwyf/pyandi>`__, whenever a new `tag is pushed to github <https://github.com/pwyf/pyandi/tags>`__.

License
-------

This work is `MIT licensed <https://github.com/pwyf/pyandi/blob/master/LICENSE.md>`__.
