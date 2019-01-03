from os.path import abspath, dirname
import shutil
import tempfile
from unittest import TestCase

import pytest

from pyandi.standard.codelist import CodelistSet
from pyandi.utils.exceptions import NoCodelistsError


class TestNoCodelists(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def test_no_codelists(self):
        with pytest.raises(NoCodelistsError):
            CodelistSet(path=self.empty_path)

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)
