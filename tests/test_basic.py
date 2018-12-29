from datetime import datetime
from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

import pytest

import pyandi
from pyandi.utils.exceptions import NoDataError


class TestNoData(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def test_no_data(self):
        with pytest.raises(NoDataError):
            pyandi.data(self.empty_path)

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)


class TestRegistry(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    def test_last_updated(self, *args):
        with pytest.warns(UserWarning, match=r'last updated \d+ days'):
            registry = pyandi.data(self.registry_path)
        assert registry.last_updated == datetime(2015, 12, 28, 3, 57, 19)
