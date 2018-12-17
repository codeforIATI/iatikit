from ..utils.abstract import GenericSet
import json
from os.path import join


class CodelistSet(GenericSet):
    def __init__(self, path=None, **kwargs):
        super().__init__()
        self._wheres = kwargs
        self._key = 'name'
        self._filters = ['version', 'name']
        if not path:
            path = join('__pyandicache__', 'standard', 'codelists')
        self.path = path

    def __iter__(self):
        version = self._wheres.get('version')
        if version:
            version = str(version)
        slug = self._wheres.get('name')
        with open(join(self.path, 'codelists.json')) as f:
            codelists = json.load(f)
        for codelist_slug, codelist_versions in codelists.items():
            if 'non-embedded' in codelist_versions:
                current_version = ['non-embedded']
            else:
                if version is None:
                    current_version = codelist_versions
                else:
                    if version in codelist_versions:
                        current_version = [version]
                    else:
                        continue
            if slug is not None and slug != codelist_slug:
                continue
            yield Codelist(codelist_slug, self.path, current_version)


class Codelist(GenericSet):
    def __init__(self, slug, path, versions, **kwargs):
        super().__init__()
        self._wheres = kwargs
        self._key = 'code'
        self._filters = ['code']
        self.slug = slug
        self.paths = {
            version: join(path, version.replace('.', ''), slug + '.json')
            for version in versions
        }
        self._versions = versions
        self.__data = {}

    @property
    def _data(self):
        if not self.__data:
            for version, path in self.paths.items():
                with open(path) as f:
                    data = json.load(f)
                data['data'] = {d['code']: d for d in data['data']}
                self.__data[version] = data
        return self.__data

    @property
    def data(self):
        return self._data[self._versions[0]]['data']

    @property
    def metadata(self):
        attributes = self._data[self._versions[0]]['attributes']
        metadata = self._data[self._versions[0]]['metadata']
        return dict(attributes, **metadata)

    def __iter__(self):
        code = self._wheres.get('code')
        if code is not None:
            code = str(code)
        for version in self._versions:
            for data in self._data[version]['data'].values():
                if code is not None and data['code'] != code:
                    continue
                yield CodelistItem(self, **data)

    def __repr__(self):
        return '<{} ({})>'.format(
            self.__class__.__name__,
            self.slug)

    @property
    def url(self):
        return self.metadata['url']

    @property
    def name(self):
        return self.metadata['name']

    @property
    def description(self):
        return self.metadata['description']

    @property
    def complete(self):
        return self.metadata['complete']


class CodelistItem:
    def __init__(self, codelist, **kwargs):
        self._category = kwargs.get('category')
        self.status = kwargs.get('status', 'active')
        self.code = kwargs.get('code')
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.codelist = codelist

    def __repr__(self):
        return '<{} ({} ({}))>'.format(
            self.__class__.__name__,
            self.name,
            self.code)
