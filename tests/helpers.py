import json
from os.path import abspath, dirname, join
import re


class CodelistMockRequest():
    def __init__(self, url):
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'codelist_downloads')

        match = re.search(r'(\d{3}).*?/([^\.\/]+)\.(csv|json)', url)
        if match:
            version, name, extension = match.groups()
            fname = '{name}-v{version}.{extension}'.format(
                name=name,
                version=version,
                extension=extension)
        else:
            raise NotImplementedError()
        self.filepath = join(codelist_path, fname)

    def json(self):
        with open(self.filepath) as handler:
            return json.load(handler)

    def iter_lines(self):
        with open(self.filepath, 'rb') as handler:
            return handler.readlines()
