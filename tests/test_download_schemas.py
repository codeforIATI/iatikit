import json
from os.path import abspath, dirname, exists, join
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from pyandi.utils import download


XSD_TMPL = '''<?xml version="1.0" encoding="utf-8"?>

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <xsd:annotation>
    <xsd:documentation xml:lang="en">
        {filename}
    </xsd:documentation>
  </xsd:annotation>
'''


class MockRequest():
    def __init__(self, url, stream=False):
        filename = url.rsplit('/', 1)[-1]
        if filename == 'Version.json':
            codelist_path = join(dirname(abspath(__file__)),
                                 'fixtures', 'codelists', 'download')
            self.filepath = join(codelist_path, filename)
        self.content = XSD_TMPL.format(filename=filename).encode()

    def json(self):
        with open(self.filepath) as f:
            return json.load(f)


class TestDownloadCodelists(TestCase):
    def setUp(self):
        self.schema_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    @patch('requests.get', MockRequest)
    def test_download_data(self):
        download.schemas(self.schema_path)

        filenames = [
            'iati-activities-schema.xsd', 'iati-organisations-schema.xsd',
            'iati-common.xsd', 'xml.xsd',
        ]
        for version in ['201', '105', '104', '103', '102', '101']:
            for filename in filenames:
                filepath = join(self.schema_path, version, filename)
                assert exists(filepath)
                with open(filepath) as f:
                    contents = f.read()
                assert contents == XSD_TMPL.format(filename=filename)

    def tearDown(self):
        shutil.rmtree(self.schema_path, ignore_errors=True)
