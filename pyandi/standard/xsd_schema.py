from os.path import exists, join

from lxml import etree

from ..utils.exceptions import SchemaNotFoundError
from ..utils.validator import Validator
from ..utils.config import CONFIG


class XSDSchema(object):
    def __init__(self, filetype, version):
        self.filetype = filetype
        self.version = version

        schema = {
            'activity': 'iati-activities-schema.xsd',
            'organisation': 'iati-organisations-schema.xsd',
        }.get(filetype)

        version_path = version.replace('.', '')
        self.schema_path = join(CONFIG['paths']['standard'], 'schemas',
                                version_path, schema)

        if not exists(self.schema_path):
            msg = 'No {filetype} schema found for IATI version "{version}".'
            msg = msg.format(filetype=filetype, version=version)
            raise SchemaNotFoundError(msg)

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
        schema = etree.XMLSchema(etree.parse(self.schema_path))
        is_valid = self.schema.validate(dataset.etree)
        error_log = ['{}: {}'.format(e.type_name, e.message)
                     for e in self.schema.error_log]
        return Validator(is_valid, error_log)
