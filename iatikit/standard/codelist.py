import json
from os.path import exists, join

from ..utils.abstract import GenericSet
from ..utils.exceptions import NoCodelistsError
from ..utils.config import CONFIG


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

    def __eq__(self, value):
        if isinstance(value, CodelistItem):
            return self.code == value.code and \
                   self.codelist.slug == value.codelist.slug
        else:
            return self.code == str(value)

    def __ne__(self, value):
        return not self.__eq__(value)


class Codelist(GenericSet):
    _key = 'code'
    _filters = ['code', 'name', 'version', 'category']
    _instance_class = CodelistItem

    def __init__(self, slug, version, **kwargs):
        super(Codelist, self).__init__()
        self.wheres = kwargs
        self.slug = slug
        self.path = join(CONFIG['paths']['standard'],
                         'codelists', slug + '.json')
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
        name = self.wheres.get('name')
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
            if name is not None and data['name'] != name:
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
        return self.metadata.get('url')

    @property
    def name(self):
        return self.metadata.get('name')

    @property
    def description(self):
        return self.metadata.get('description')

    @property
    def complete(self):
        return self.attributes.get('complete') == '1'


class CodelistSet(GenericSet):
    _key = 'slug'
    _filters = ['slug', 'version']
    _instance_class = Codelist

    def __init__(self, **kwargs):
        super(CodelistSet, self).__init__()
        self.wheres = kwargs
        self.path = join(CONFIG['paths']['standard'], 'codelists')
        if not exists(join(self.path, 'codelists.json')):
            error_msg = 'Error: No codelists found! ' + \
                          'Download fresh codelists ' + \
                          'using:\n\n   ' + \
                          '>>> iatikit.download.codelists()\n'
            raise NoCodelistsError(error_msg)

    def __iter__(self):
        version = self.wheres.get('version')
        if version:
            version = str(version)
        slug = self.wheres.get('slug')
        with open(join(self.path, 'codelists.json')) as handler:
            all_codelists = json.load(handler)
        for codelist_slug, codelist_versions in all_codelists.items():
            if version is not None and version not in codelist_versions:
                continue

            if slug is not None and slug != codelist_slug:
                continue

            yield Codelist(codelist_slug, version)


def codelists():
    """Helper function for fetching all codelists."""
    return CodelistSet()
