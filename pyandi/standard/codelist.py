from collections import UserDict
import json
from os import listdir
from os.path import exists, join, splitext

from ..utils.exceptions import UnknownCodelistException


class Codelist(UserDict):
    def __init__(self, slug, path, version):
        self.slug = slug
        self.version = version
        self.filepath = join(path, slug + '.json')
        if not exists(self.filepath):
            raise UnknownCodelistException('Codelist not found')

    def __iter__(self):
        for k in self.all().keys():
            yield k

    def __len__(self):
        return len(self.all())

    def __repr__(self):
        return '<{} ({} v{})>'.format(
            self.__class__.__name__,
            self.slug,
            self.version)

    def _load(self):
        if hasattr(self, 'data'):
            return
        with open(self.filepath) as f:
            j = json.load(f)
        self._url = j['metadata']['url']
        self._name = j['metadata']['name']
        self._description = j['metadata']['description']
        self._complete = j['attributes']['complete']
        self.data = {x['code']: x['name'] for x in j['data']}

    @property
    def url(self):
        self._load()
        return self._url

    @property
    def name(self):
        self._load()
        return self._name

    @property
    def description(self):
        self._load()
        return self._description

    @property
    def complete(self):
        self._load()
        return self._complete

    def all(self):
        self._load()
        return self.data

    def get(self, code):
        return self.all().get(code)

    def __getitem__(self, code):
        return self.all()[code]


def get(slug, path=None, version='latest'):
    if not path:
        path = join('__pyandicache__', 'standard', 'codelists')
    if version == 'latest':
        major = max(listdir(path))
        path = join(path, major)
    else:
        major = version.split('.')[0]
        path = join(path, major)
    return Codelist(slug, path, major)


def all(path=None, version='latest'):
    if not path:
        path = join('__pyandicache__', 'standard', 'codelists')
    if version == 'latest':
        major = max(listdir(path))
        path = join(path, major)
    else:
        major = version.split('.')[0]
        path = join(path, major)
    return [Codelist(splitext(slug)[0], path, major) for slug in listdir(path)]
