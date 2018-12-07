from os.path import basename, splitext
from glob import glob
import json

from lxml import etree

from ..abstract import PyandiSet
from .activity import ActivitySet


class DatasetSet(PyandiSet):
    def __init__(self, data_path, metadata_path, **kwargs):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._wheres = kwargs

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(self.metadata_path))
        paths = zip(data_paths, metadata_paths)

        where_name = self._wheres.get('name')
        if where_name:
            paths = filter(
                lambda x: splitext(basename(x[0]))[0] == where_name, paths)

        for data_path, metadata_path in paths:
            yield Dataset(data_path, metadata_path)


class Dataset:
    def __init__(self, data_path, metadata_path):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._xml = None

    @property
    def name(self):
        return splitext(basename(self.data_path))[0]

    @property
    def xml(self):
        if not self._xml:
            self._xml = etree.parse(self.data_path)
        return self._xml

    @property
    def raw_xml(self):
        return etree.tostring(self.xml)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def is_valid(self):
        # TODO: This currently just checks for a valid root node
        try:
            if self.filetype:
                return True
        except etree.XMLSyntaxError:
            pass
        return False

    @property
    def metadata(self):
        with open(self.metadata_path) as f:
            return json.load(f)

    @property
    def filetype(self):
        roottag = self.xml.getroot().tag
        if roottag in ['iati-activities', 'iati-organisations']:
            return roottag
        return None

    @property
    def version(self):
        query = '//{}/@version'.format(self.filetype)
        v = self.xml.xpath(query)
        if len(v) == 1:
            return v[0]
        return None

    @property
    def activities(self):
        return ActivitySet([self])
