from os.path import abspath, dirname
import shutil
import tempfile
from unittest import TestCase

import pytest

import pyandi
from pyandi.utils.exceptions import NoDataError


class TestShortcuts(TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def test_no_data(self):
        with pytest.raises(NoDataError):
            pyandi.data(self.path)

    def tearDown(self):
        shutil.rmtree(self.path, ignore_errors=True)
