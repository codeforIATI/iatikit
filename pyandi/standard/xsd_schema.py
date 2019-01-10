import logging
import os.path

from lxml import etree

from ..utils.exceptions import SchemaNotFoundError


class XSDSchema(object):
    def __init__(self, filetype, version, path=None):
        self.filetype = filetype
        self.version = version

        schema = {
            'activity': 'iati-activities-schema.xsd',
            'organisation': 'iati-organisations-schema.xsd',
        }.get(filetype)

        version_path = version.replace('.', '')
        if not path:
            path = os.path.join('__pyandicache__', 'standard', 'schemas')
        schema_path = os.path.join(path, version_path, schema)

        if not os.path.exists(schema_path):
            msg = 'No {filetype} schema found for IATI version "{version}".'
            msg = msg.format(filetype=filetype, version=version)
            raise SchemaNotFoundError(msg)

        self.schema = etree.XMLSchema(etree.parse(schema_path))

    def __repr__(self):
        return '<{} ({} {})>'.format(self.__class__.__name__,
                                     self.filetype, self.version)

    def validate(self, dataset):
        is_valid = self.schema.validate(dataset.etree)
        if not is_valid:
            for error in self.schema.error_log:
                logging.warning('%s / %s', error.type_name, error.message)
        return is_valid
