# iatikit

[![PyPI Package latest release](https://img.shields.io/pypi/v/iatikit.svg)](https://pypi.org/project/iatikit/)
[![License](https://img.shields.io/pypi/l/iatikit.svg)](https://pypi.org/project/iatikit/)
[![Supported versions](https://img.shields.io/pypi/pyversions/iatikit.svg)](https://pypi.org/project/iatikit/)
[![Build Status](https://github.com/codeforIATI/iati-datastore/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/codeforIATI/iati-datastore/actions/workflows/ci.yml)
[![Test coverage](https://img.shields.io/coveralls/github/codeforIATI/iatikit/main.svg)](https://coveralls.io/github/codeforIATI/iatikit?branch=main)

iatikit is a toolkit for using [IATI data](https://iatistandard.org/). It includes a query language wrapper around [XPath](https://en.wikipedia.org/wiki/XPath), to make dealing with disparate IATI versions easier.

The name was inspired by [Open Contracting](https://www.open-contracting.org/)'s [ocdskit](https://pypi.org/project/ocdskit/).

## Installation

iatikit is tested for pythons 3.7 – 3.14.

You can install it using `pip`:

```sh
pip install iatikit
```

## Documentation

Check out [Read the Docs](https://iatikit.readthedocs.io)!

## Roadmap

The [github issue tracker](https://github.com/codeforIATI/iatikit/issues) will hopefully provide some idea.

## Development

You can set up a local version by creating a virtualenv and running:

```sh
pip install -r requirements_dev.txt
```

You can run tests with:

```sh
pytest
```

## Deployment

iatikit is [deployed to pypi](https://pypi.org/project/iatikit/) automatically by GitHub Actions whenever a new [tag is pushed to github](https://github.com/codeforIATI/iatikit/tags).

## License

This work is [MIT licensed](https://github.com/codeforIATI/iatikit/blob/main/LICENSE.md).
