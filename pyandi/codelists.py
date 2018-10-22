import json
from glob import glob
from os.path import join


class Codelist:
    def __init__(self, name):
        self.path = join('__pyandicache__', 'codelists')
        files = glob(join(self.path, '*', '*'))
        self.filename = name + '.json'
        codelist_files = list(filter(
            lambda x: x.split('/')[-1] == self.filename, files))
        if codelist_files == []:
            raise Exception('Codelist not found')
        self.versions = [x.split('/')[2] for x in codelist_files]
        self._codelist = {}

    def __iter__(self):
        for k, v in self.all().items():
            yield (k, v)

    def _load(self, version='latest'):
        if version == 'latest':
            version = max(self.versions)
        with open(join(self.path, version, self.filename)) as f:
            j = json.load(f)
        self._codelist[version] = {x['code']: x['name'] for x in j['data']}
        self._url = j['metadata']['url']
        self._name = j['metadata']['name']
        self._description = j['metadata']['description']
        self._complete = j['attributes']['complete']

    def all(self, version='latest'):
        if version == 'latest':
            version = max(self.versions)
        if version not in self._codelist:
            self._load(version)
        return self._codelist[version]

    def get(self, code, version='latest'):
        return self.all(version).get(code)


class CodelistSetMeta(type):
    def __getattr__(cls, codelist_name):
        return Codelist(codelist_name)


class CodelistSet(metaclass=CodelistSetMeta):
    pass
