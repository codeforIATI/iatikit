import json
from os.path import join, exists

from ..utils.abstract import GenericSet
from ..utils.exceptions import NoCodelistsError
from ..utils import download


class CodelistSet(GenericSet):
    def __init__(self, path=None, **kwargs):
        super().__init__()
        self._key = 'name'
        self._filters = ['name', 'version']
        self._wheres = kwargs
        self._instance_class = Codelist

        if not path:
            path = join('__pyandicache__', 'standard', 'codelists')
        self.path = path
        if not exists(self.path):
            error_msg = 'Error: No codelists found! ' + \
                          'Download fresh codelists ' + \
                          'using:\n\n   ' + \
                          '>>> pyandi.download.codelists()\n'
            raise NoCodelistsError(error_msg)

    def __iter__(self):
        version = self._wheres.get('version')
        if version:
            version = str(version)
        slug = self._wheres.get('name')
        with open(join(self.path, 'codelists.json')) as f:
            codelists = json.load(f)
        for codelist_slug, codelist_versions in codelists.items():
            if 'non-embedded' in codelist_versions:
                current_version = None
            else:
                if version is not None and version not in codelist_versions:
                    continue
                current_version = version
            if slug is not None and slug != codelist_slug:
                continue
            yield Codelist(codelist_slug, self.path, current_version)

    def download(self):
        return download.codelists(self.path)


class Codelist(GenericSet):
    def __init__(self, slug, path, version, **kwargs):
        super().__init__()
        self._key = 'code'
        self._filters = ['code', 'version']
        self._wheres = kwargs
        self._instance_class = CodelistItem

        self.slug = slug
        self.path = join(path, slug + '.json')
        self.version = version
        self.__data = None

    @property
    def _data(self):
        if not self.__data:
            with open(self.path) as f:
                self.__data = json.load(f)
        return self.__data

    @property
    def data(self):
        return self._data['data']

    @property
    def metadata(self):
        attributes = self._data['attributes']
        metadata = self._data['metadata']
        return dict(attributes, **metadata)

    def __iter__(self):
        code = self._wheres.get('code')
        version = self._wheres.get('version', self.version)
        if version is not None:
            version = str(version)
        if code is not None:
            code = str(code)
        for data in self.data.values():
            if code is not None and data['code'] != code:
                continue
            if version is not None:
                version_from = data.get('from')
                version_until = data.get('until')
                if version_from and version_until and \
                        (version < version_from or
                         version > version_until):
                    continue
            yield CodelistItem(self, **data)

    def __repr__(self):
        if self.version:
            slug = '{} v{}'.format(self.slug, self.version)
        else:
            slug = self.slug
        return '<{} ({})>'.format(self.__class__.__name__, slug)

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
