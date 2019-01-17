import json
from os.path import abspath, dirname, exists, join
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from iatikit.utils import download
from iatikit.utils.config import CONFIG


XSD_TMPL = '''<?xml version="1.0" encoding="utf-8"?>

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <xsd:annotation>
    <xsd:documentation xml:lang="en">
        {filename}
    </xsd:documentation>
  </xsd:annotation>
'''


class MockRequest():
    def __init__(self, url):
        filename = url.rsplit('/', 1)[-1]
        if filename == 'Version.json':
            self.filepath = join(dirname(abspath(__file__)),
                                 'fixtures', 'codelist_downloads',
                                 'Version-v201.json')
        self.content = XSD_TMPL.format(filename=filename).encode()

    def json(self):
        with open(self.filepath) as handler:
            return json.load(handler)


class TestDownloadSchemas(TestCase):
    def setUp(self):
        self.standard_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))
        config_dict = {'paths': {'standard': self.standard_path}}
        CONFIG.read_dict(config_dict)

    @patch('requests.get', MockRequest)
    def test_download_schemas(self):
        download.schemas()

        filenames = [
            'iati-activities-schema.xsd', 'iati-organisations-schema.xsd',
            'iati-common.xsd', 'xml.xsd',
        ]
        for version in ['201', '105', '104', '103', '102', '101']:
            for filename in filenames:
                filepath = join(self.standard_path, 'schemas',
                                version, filename)
                assert exists(filepath)
                with open(filepath) as handler:
                    contents = handler.read()
                assert contents == XSD_TMPL.format(filename=filename)

    def tearDown(self):
        shutil.rmtree(self.standard_path, ignore_errors=True)
