import json
import os.path

from ..utils.abstract import GenericSet
from ..utils.exceptions import NoCodelistsError
from ..utils import download


class CodelistItem(object):
    def __init__(self, codelist, **kwargs):
        self.category = kwargs.get('category')
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


class Codelist(GenericSet):
    _key = 'code'
    _filters = ['code', 'version', 'category']
    _instance_class = CodelistItem

    def __init__(self, slug, path, version, **kwargs):
        super(Codelist, self).__init__()
        self.wheres = kwargs
        # self._instance_class = CodelistItem

        self.slug = slug
        self.path = os.path.join(path, slug + '.json')
        self.version = version
        self.__data = None

    @property
    def _data(self):
        if not self.__data:
            with open(self.path) as handler:
                self.__data = json.load(handler)
        return self.__data

    @property
    def data(self):
        return self._data['data']

    @property
    def attributes(self):
        return self._data['attributes']

    @property
    def metadata(self):
        return self._data['metadata']

    def __iter__(self):
        code = self.wheres.get('code')
        category = self.wheres.get('category')
        version = self.wheres.get('version', self.version)
        if version is not None:
            version = str(version)
        if code is not None:
            code = str(code)
        if category is not None:
            category = str(category)
        for data in self.data.values():
            if code is not None and data['code'] != code:
                continue
            if category is not None and data['category'] != category:
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
        return self.attributes['complete'] == '1'


class CodelistSet(GenericSet):
    _key = 'slug'
    _filters = ['slug', 'version']
    _instance_class = Codelist

    def __init__(self, path=None, **kwargs):
        super(CodelistSet, self).__init__()
        self.wheres = kwargs

        if not path:
            path = os.path.join('__pyandicache__', 'standard', 'codelists')
        self.path = path
        if not os.path.exists(os.path.join(self.path, 'codelists.json')):
            error_msg = 'Error: No codelists found! ' + \
                          'Download fresh codelists ' + \
                          'using:\n\n   ' + \
                          '>>> pyandi.download.codelists()\n'
            raise NoCodelistsError(error_msg)

    def __iter__(self):
        version = self.wheres.get('version')
        if version:
            version = str(version)
        slug = self.wheres.get('slug')
        with open(os.path.join(self.path, 'codelists.json')) as handler:
            all_codelists = json.load(handler)
        for codelist_slug, codelist_versions in all_codelists.items():
            if version is not None and version not in codelist_versions:
                continue

            if slug is not None and slug != codelist_slug:
                continue

            yield Codelist(codelist_slug, self.path, version)

    def download(self):
        return download.codelists(self.path)


def codelists(path=None):
    """Helper function for fetching all codelists."""
    return CodelistSet(path)
