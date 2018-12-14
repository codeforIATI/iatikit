from ..utils.abstract import GenericSet
import json
from os.path import join


class CodelistSet(GenericSet):
    def __init__(self, path=None, **kwargs):
        super().__init__()
        self._wheres = kwargs
        self._key = 'name'
        if not path:
            path = join('__pyandicache__', 'standard', 'codelists')
        self.path = path

    def __iter__(self):
        version = self._wheres.get('version')
        if version:
            version = str(version).split('.')[0]
        slug = self._wheres.get('name')
        with open(join(self.path, 'codelists.json')) as f:
            codelists = json.load(f)
        for codelist_slug, codelist_versions in codelists.items():
            if version is not None and version not in codelist_versions:
                continue
            if slug is not None and slug != codelist_slug:
                continue
            codelist_versions = [version] if version else codelist_versions
            yield Codelist(codelist_slug, self.path, codelist_versions)


class Codelist(GenericSet):
    def __init__(self, slug, path, versions, **kwargs):
        super().__init__()
        self._wheres = kwargs
        self._key = 'code'
        self.slug = slug
        self.paths = {version: join(path, version, slug + '.json')
                      for version in versions}
        self.versions = versions
        self._data = {}

    @property
    def data(self):
        if not self._data:
            for version, path in self.paths.items():
                with open(path) as f:
                    data = json.load(f)
                data['data'] = {d['code']: d for d in data['data']}
                self._data[version] = data
        return self._data

    def __iter__(self):
        code = self._wheres.get('code')
        for version in self.versions[::-1]:
            for data in self.data[version]['data'].values():
                if code and data['code'] != code:
                    continue
                yield CodelistCode(**data)

    def __repr__(self):
        return '<{} ({} v{})>'.format(
            self.__class__.__name__,
            self.slug,
            ','.join(self.versions))

    @property
    def url(self):
        return self.data[self.versions[-1]]['metadata']['url']

    @property
    def name(self):
        return self.data[self.versions[-1]]['metadata']['name']

    @property
    def description(self):
        return self.data[self.versions[-1]]['metadata']['description']

    @property
    def complete(self):
        return self.data[self.versions[-1]]['attributes']['complete']


class CodelistCode:
    def __init__(self, **kwargs):
        self._category = kwargs.get('category')
        self.status = kwargs.get('status')
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')

    def __repr__(self):
        return '<{} ({} ({}))>'.format(
            self.__class__.__name__,
            self.name,
            self.code)
